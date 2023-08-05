import logging
import os
from datetime import datetime, timedelta
from typing import Any, AnyStr, Dict, List, Optional, Tuple, TypedDict
from urllib.parse import urljoin

import jwt
import requests

from ruleau.decorators import api_request
from ruleau.exceptions import (
    APIException,
    CaseAPIException,
    OrganisationalDataApiException,
    RuleAPIException,
    UiLayoutMetadataApiException,
)
from ruleau.process import Process
from ruleau.rule import Rule
from ruleau.structures import (
    ErrorMessage,
    OrganisationalData,
    OrganisationalScheme,
    UiLayoutMetadata,
)

logger = logging.getLogger(__name__)


class OrganisationalDataRow(TypedDict):
    key: str
    value: Any


class ReexecutionType(TypedDict):

    process_id: str
    case_id: str
    last_override_time: datetime


class ApiAdapter:
    base_url: AnyStr
    base_path: AnyStr
    username: Optional[AnyStr]
    password: Optional[AnyStr]
    organisational_data: Optional[List[OrganisationalData]]

    def __init__(
        self,
        base_url: AnyStr,
        username: Optional[AnyStr] = None,
        password: Optional[AnyStr] = None,
    ):
        """
        :param base_url: Base URL of the ruleau API
        :param username: (Optional) Users username
        :param password: (Optional) Users password
        """
        self.base_url = base_url
        self.base_path = "/api/v1/"

        self.username = os.getenv("RULEAU_USERNAME", username)
        self.password = os.getenv("RULEAU_PASSWORD", password)
        if not self.username or not self.password:
            raise ValueError("Username or Password not supplied")
        self.organisational_data = None

        self.access_token = None
        self.refresh_token = None
        self.access_token_expiry = None
        self.session = None
        self._fetch_jwt_token()

    def with_organisational_data(
        self, organisational_data: Optional[List[Dict]] = None
    ) -> "ApiAdapter":
        """
        Adds organisational_data to the ApiAdapter object.
        :param organisational_data: Organisation-specific data for display
        """
        self.organisational_data = organisational_data
        return self

    @api_request
    def sync_case(
        self,
        case_id: AnyStr,
        process_id: AnyStr,
        payload: Dict,
    ) -> Dict:
        """
        Synchronise case with API. Includes previously-saved organisational data which
        is cleared after sending.
        :param case_id: The ID of the case being executed
        :param process_id: The ID of the process
        :param payload: Case payload to execute on
        :return:
        """

        data = {
            "id": case_id,
            "process": process_id,
            "organisational_data": self.organisational_data,
            "payload": payload,
            "status": "OPEN",
            "execution_status": "EXECUTING",
        }

        response = self.session.post(
            urljoin(self.base_url, f"{self.base_path}processes/{process_id}/cases"),
            headers={"Authorization": f"Bearer {self.access_token}"},
            json=data,
        )

        # Clear organisation data to prevent adding it where it doesn't belong.
        self.organisational_data = None

        if response.status_code != 200:
            raise CaseAPIException(
                activity="create", case_id=case_id, response=response
            )

        return response.json()

    @api_request
    def publish_organisational_scheme(
        self, rule: Rule, organisational_scheme: List[OrganisationalScheme]
    ) -> List[Dict]:
        """
        Sets the organisational data fields that can be attached to a Process.
        :param rule: The rule used to identify the Process the fields relate to.
        :param organisational_scheme: The fields to set for the process.
        :return: The organisational schemes stored in the API.
        """
        process = Process.create_process_from_rule(rule)
        self.sync_process(process)

        url = urljoin(
            self.base_url,
            f"{self.base_path}processes/{process.id}/organisational_scheme",
        )

        response = self.session.post(
            url,
            json=organisational_scheme,
        )

        if response.status_code != 201:
            raise OrganisationalDataApiException(
                process_id=process.id, response=response
            )

        return response.json()

    @api_request
    def publish_ui_layout_metadata(
        self, rule: Rule, ui_layout_metadata: UiLayoutMetadata
    ) -> Dict:
        """
        Stores the order by which fields declared in the organisational scheme
        for a given Process should appear on both the Cases and Overrides screens.
        Any fields not specified in the layout metadata will appear after fields that
        are, ordered by the date they were created.
        :param rule: The rule used to identify the Process the fields relate to.
        :param ui_layout_metadata: Defines the order the fields should appear.
        :return: The metadata stored in the API.
        """
        process = Process.create_process_from_rule(rule)

        url = urljoin(
            self.base_url,
            f"{self.base_path}processes/{process.id}/ui_layout_metadata",
        )

        case_org_data_order = (
            [x["id"] for x in ui_layout_metadata["case_org_data_order"]]
            if "case_org_data_order" in ui_layout_metadata
            else []
        )

        override_org_data_order = (
            [x["id"] for x in ui_layout_metadata["override_org_data_order"]]
            if "override_org_data_order" in ui_layout_metadata
            else []
        )

        data_payload_presentation = (
            ui_layout_metadata["data_payload_presentation"]
            if "data_payload_presentation" in ui_layout_metadata
            else None
        )

        response = self.session.post(
            url,
            json={
                "case_org_data_order": case_org_data_order,
                "override_org_data_order": override_org_data_order,
                "data_payload_presentation": data_payload_presentation,
            },
        )

        if response.status_code != 201:
            raise UiLayoutMetadataApiException(process_id=process.id, response=response)

        return response.json()

    @api_request
    def sync_process(self, process: Process):

        response = self.session.post(
            urljoin(self.base_url, f"{self.base_path}processes"),
            json=process.parse(),
        )

        if response.status_code != 201:
            raise RuleAPIException(
                activity="save", process_id=process.id, response=response
            )

        return response.json()

    def sync_results(
        self,
        process: "Process",
        case_id: AnyStr,
    ):

        self._sync_results(
            process.rules,
            process.id,
            case_id,
            error=process.error,
            data_override_changes=process.data_override_changes,
        )

    @api_request
    def _sync_results(
        self,
        rules: list[Rule],
        process_id: AnyStr,
        case_id: AnyStr,
        error: Optional[ErrorMessage] = None,
        data_override_changes: Dict = None,
    ):
        payload = {
            "result": [
                {
                    "rule": rule.id,
                    "result": rule.execution_result.result,
                    "payloads": rule.execution_result.payload.accessed
                    if rule.execution_result.payload
                    else None,
                    "override": rule.execution_result.override,
                    "original_result": rule.execution_result.original_result,
                    "skipped": rule.execution_result.skipped,
                }
                for rule in rules
                if rule.execution_result
            ]
        }

        if error:
            payload["error"] = error

        if data_override_changes:
            payload["data_override_changes"] = data_override_changes

        response = self.session.post(
            urljoin(
                self.base_url,
                f"{self.base_path}processes/{process_id}/cases/" f"{case_id}/results",
            ),
            json=payload,
        )

        if response.status_code > 299:
            raise RuleAPIException(
                activity="store rule result for",
                process_id=process_id,
                response=response,
            )
        return None

    @api_request
    def fetch_data_overrides(
        self, case_id: AnyStr, process_id: AnyStr
    ) -> Optional[Dict[AnyStr, Any]]:
        """
        Fetch data overrides
        :param case_id: client ID that identifies a previously established case
        :param process_id: The ID of the process that the case is being run against
        :return: a ruleau data override Optional[Dict[AnyStr, Any]]
        """

        response = self.session.get(
            urljoin(
                self.base_url,
                f"{self.base_path}processes/{process_id}/"
                f"cases/{case_id}/data_overrides",
            ),
        )

        if response.status_code == 404:
            return {}

        if response.status_code != 200:
            message = (
                "Could not fetch data overrides, "
                f"status code: {response.status_code}, "
                f"error message {response.text}"
            )

            raise APIException(message)

        return response.json()

    @api_request
    def fetch_override(
        self, case_id: AnyStr, process_id: AnyStr, rule_id: AnyStr
    ) -> Optional[Dict[AnyStr, Any]]:
        """
        Fetch specific rule override
        :param case_id: client ID that identifies a previously established case
        :param process_id: The ID of the process that the case is being run against
        :param rule_id: The ID of the Rule to fetch overrides for
        :return: a ruleau overrides Optional[Dict[AnyStr, Any]]
        """
        response = self.session.get(
            urljoin(
                self.base_url,
                f"{self.base_path}processes/{process_id}/"
                f"cases/{case_id}/overrides/search",
            ),
            params={"rule_id": rule_id},
        )

        if response.status_code == 404:
            return {}

        if response.status_code != 200:
            message = (
                f"Could not fetch override for {process_id},{case_id} "
                f"status code: {response.status_code}, "
                f"error message {response.text}"
            )

            raise APIException(message)

        return response.json()

    @api_request
    def fetch_all_overrides(
        self, case_id: AnyStr, process_id: AnyStr
    ) -> Dict[Tuple, Any]:
        """
        Fetch all rule overrides and store in self.rule_overrides
        :param case_id: client ID that identifies a previously established case
        :param process_id: The ID of the process that the case is being run against
        """

        response = self.session.get(
            urljoin(
                self.base_url,
                f"{self.base_path}processes/{process_id}/" f"cases/{case_id}/overrides",
            ),
        )

        if response.status_code != 200:
            raise APIException(
                "Unable to fetch overrides from API. Status code: "
                f"{response.status_code}"
            )

        rule_overrides = {}
        for override in [o for o in response.json() if "id" in o]:
            key = (case_id, process_id, override["id"])
            rule_overrides[key] = override

        return rule_overrides

    def _fetch_jwt_token(self):
        """
        Fetches the JWT token for the username and password provided
        """
        login_response = requests.post(
            urljoin(self.base_url, f"{self.base_path}token/"),
            data={"username": self.username, "password": self.password},
        )
        if login_response.status_code != 200:
            raise requests.exceptions.RequestException(login_response.json())

        body = login_response.json()
        self.access_token = body["access"]
        self.refresh_token = body["refresh"]
        self._set_access_token_expiry(body)

    def _set_access_token_expiry(self, body):
        """
        Decodes the expiry time for the access token
        """
        access_payload = jwt.decode(body["access"], options={"verify_signature": False})
        self.access_token_expiry = datetime.fromtimestamp(int(access_payload["exp"]))

    def _refresh_access_token(self):
        """
        Gets a new access token using the refresh token
        """

        refresh_response = requests.post(
            urljoin(self.base_url, f"{self.base_path}token/refresh/"),
            data={
                "refresh": self.refresh_token,
            },
        )
        if refresh_response.status_code != 200:
            raise requests.exceptions.RequestException(refresh_response.json())

        body = refresh_response.json()
        self.access_token = body["access"]
        self._set_access_token_expiry(body)

    def _check_access_token_is_active(self):
        """
        Checks to see if the access token is close to expiring (within 5 seconds)
        or has expired
        """
        time_now = datetime.now()
        if time_now > (self.access_token_expiry - timedelta(seconds=5)):
            self._refresh_access_token()

    def _create_requests_session(self):
        self.session = requests.session()
        self.session.headers.update({"Authorization": f"Bearer {self.access_token}"})

    @api_request
    def fetch_cases_for_reexecution(self) -> [ReexecutionType]:

        response = self.session.get(
            urljoin(
                self.base_url,
                f"{self.base_path}cases/reexecution",
            ),
        )
        if response.status_code != 200:
            return []
        return response.json()
