import json
import logging
import re
from typing import TYPE_CHECKING, Any, AnyStr, Dict, List, Optional

from jsonpath_ng import parse

from ruleau.adapter import ApiAdapter
from ruleau.exceptions import (
    AttributeDoesntExist,
    CaseIdRequiredException,
    DataOverrideBase,
    DataOverrideException,
    DuplicateRuleIdException,
    DuplicateRuleNameException,
    PayloadFormatException,
)
from ruleau.process import Process
from ruleau.rule import Rule

if TYPE_CHECKING:
    from ruleau.structures import ExecutionResult

list_action_finder = re.compile(r"\[[\d\*]+\]$")
index_extractor = re.compile(r"\[([^\[\]]*)\]")

logger = logging.getLogger(__name__)


def validate_no_duplicate_rule_names(rules: List[Rule]) -> None:
    """Returns True if there are no duplicate Rule Names are used
    A name can only be re-used if the same rule is included multiple times
    """
    rules_dict = {}
    for rule in rules:
        if rule.name not in rules_dict:
            rules_dict[rule.name] = rule
        else:
            if rule != rules_dict[rule.name]:
                raise DuplicateRuleNameException(rule, rules_dict[rule.name])


def validate_no_duplicate_rule_ids(rules: List[Rule]) -> None:
    """Returns True if there are no duplicate Rule IDs used
    An ID can only be re-used if the same rule is included multiple times
    """
    rules_dict = {}
    for rule in rules:
        if rule.id not in rules_dict:
            rules_dict[rule.id] = rule
        else:
            if rule != rules_dict[rule.id]:
                raise DuplicateRuleIdException(rule, rules_dict[rule.id])


def get_case_id_from_json_path(
    payload: Dict[AnyStr, Any],
    case_id_jsonpath: AnyStr,
) -> Optional[str]:
    """
    Return case_id value from json payload

    :param payload Dict[AnyStr, Any]: Raise
    :param case_id_jsonpath AnyStr: The json path to the case_id in the payload
    :rtype Optional[str]: The case_id from the payload (or None if no path provided)
    :raises ValueError: If provided JSON path not found
    :raises ValueError: If the case_id at the path is blank (empty string)
    """
    # If jsonpath is None, then there is no case_id
    if case_id_jsonpath is None:
        return None

    # Otherwise find the case id in the json
    case_id_results = parse(case_id_jsonpath).find(payload)
    if not case_id_results:
        raise ValueError("Case ID not found in payload")

    case_id = str(case_id_results[0].value)
    if not case_id:
        raise ValueError("Case ID not found")

    return case_id


def extract_list_action(path: AnyStr) -> (List, Optional[AnyStr]):
    """
    Strips a path '$.path.to.my.object' in to a usable list of dictionary keys
    as well as identifying any list actions appended to the final key: e.g. the '[1]' in
    '$.path.to.my.object[1]'
    """

    list_action = list_action_finder.findall(path)
    if list_action:
        path = list_action_finder.sub("", path)
        return path, list_action[0]
    return path, None


def check_path_is_overridable_value(payload: Dict, path: AnyStr):
    """
    Checks to see if a json path is an overridable value (not a Dict or a nested list)
    """
    json_expr = parse(path)
    matches = json_expr.find(payload)
    if not matches:
        return False
    if isinstance(matches[0].value, dict):
        return False
    if isinstance(matches[0].value, list):
        return not any(isinstance(i, list) for i in matches[0].value)
    return True


def update_list(list_action: AnyStr, current_list: List, value: Any):
    """
    Updates a list depending on the action specified
    """
    # Append item to the end of the list
    if list_action == "[*]":
        current_list.append(value)
    # Append item into the index where specified
    else:
        update_at_index(current_list, list_action, value)
    return current_list


def update_at_index(current_list, list_action, value):
    index = int(index_extractor.findall(list_action)[0])
    if len(current_list) < (index + 1):
        current_list.insert(index, value)
    else:
        current_list[index] = value


def update_payload_value(
    payload: Dict,
    path: AnyStr,
    value: AnyStr,
    previous_value: AnyStr,
    list_action: Optional[AnyStr],
):
    """
    Sets a value in a nested dictionary
    """
    # Values are always stored as JSON strings
    decoded_val = json.loads(value)

    json_expr = parse(path)
    if not list_action:
        json_expr.update(payload, decoded_val)
        return
    current_list = json_expr.find(payload)[0].value
    old_value = current_list
    current_list = update_list(list_action, current_list, decoded_val)
    json_expr.update(payload, current_list)

    return old_value


def remove_null_values(payload: Dict, path: AnyStr):
    """
    Removes any occurences of "null" from a list in a dictionary
    given the jsonpath to the list
    """
    json_expr = parse(path)
    current_list = json_expr.find(payload)[0].value
    current_list = list(filter(lambda a: a is not None, current_list))
    json_expr.update(payload, current_list)


def apply_data_overrides(data_overrides: List, payload: Dict):
    """
    Applies a list of data overrides to the payload
    """
    try:
        edited_list_attributes = []
        for override in data_overrides:
            path, list_action = extract_list_action(override["target"])

            if not check_path_is_overridable_value(payload, path):
                raise AttributeDoesntExist(path)

            override["previous_value"] = update_payload_value(
                payload,
                path,
                override["value"],
                override["previous_value"],
                list_action=list_action,
            )

            if list_action:
                if path not in edited_list_attributes:
                    edited_list_attributes.append(path)
        for _keys in edited_list_attributes:
            remove_null_values(payload, _keys)
        return payload
    except DataOverrideBase as e:
        raise e
    except Exception:
        raise DataOverrideException()


def execute(
    executable_rule: Rule,
    payload: Dict[AnyStr, Any],
    process: Process,
    case_id_jsonpath: AnyStr = None,
    case_id: Optional[AnyStr] = None,
    api_adapter: Optional[ApiAdapter] = None,
) -> "ExecutionResult":
    """
    Executes the provided rule, following dependencies and
    passing in results accordingly
    """

    if not isinstance(payload, dict):
        raise PayloadFormatException()

    if api_adapter:
        case_id = (
            case_id
            if case_id is not None
            else get_case_id_from_json_path(payload, case_id_jsonpath)
        )
        if not case_id:
            raise CaseIdRequiredException(rule=executable_rule)

    # Validate unique rule name
    flattened_rules_as_objects = executable_rule.flatten_rule_objects()
    validate_no_duplicate_rule_names(flattened_rules_as_objects)

    # Validate unique rule ids
    validate_no_duplicate_rule_ids(flattened_rules_as_objects)

    # If API adapter was passed sync the case
    executable_rule.calculate_order_values()

    data_overrides = {}
    rule_overrides = {}
    if api_adapter:

        data_overrides = api_adapter.fetch_data_overrides(
            case_id=case_id, process_id=process.id
        )
        rule_overrides = api_adapter.fetch_all_overrides(
            case_id=case_id, process_id=process.id
        )

        if "payload_change" in data_overrides:
            try:
                payload = apply_data_overrides(
                    data_overrides["payload_change"], payload
                )
            except Exception as e:
                return __sync_error_to_api(
                    api_adapter, case_id, data_overrides, e, payload, process
                )

        # Sync the case
        api_adapter.sync_case(case_id=case_id, process_id=process.id, payload=payload)

    override_changes = None
    if "payload_change" in data_overrides and data_overrides["payload_change"]:
        override_changes = data_overrides["payload_change"]
    # Trigger the rule execution, from the top level rule
    return process.execute(
        case_id=case_id,
        payload=payload,
        api_adapter=api_adapter,
        data_override_changes=override_changes,
        rule_overrides=rule_overrides,
    )


def __sync_error_to_api(
    api_adapter: ApiAdapter,
    case_id: str,
    data_overrides: Dict,
    e: Exception,
    payload: Dict,
    process: Process,
):
    api_adapter.sync_case(case_id=case_id, process_id=process.id, payload=payload)
    error = {"error_name": e.__class__.__name__, "error_message": e.message}
    # We need to run the below execute as it updates the API telling it
    # that we skipped every rule for this process due to an error
    try:
        process.execute(
            case_id=case_id,
            payload=payload,
            api_adapter=api_adapter,
            setup_error=error,
            data_override_changes=data_overrides["payload_change"],
        )
    # If raise the original exception even if there an exception from the execute
    finally:
        raise e
