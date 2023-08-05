import inspect
import re
from os import path
from typing import List, Optional


def rule_exception_message(msg: str, rules_list: List) -> str:
    """Writes an extended debug message for rules-based exceptions."""
    msgs_list = []
    msg = "" if msg is None else msg
    for a_rule in rules_list:
        if a_rule is not None and hasattr(a_rule, "id"):
            msgs_list.append(
                f"Rule id {a_rule.id} on line {a_rule.line_number} in file "
                f"{a_rule.file_name}"
            )
        else:
            msgs_list.append("Unknown rule")

    return msg + " Rule detail: " + ", ".join(msgs_list)


def get_relevant_locals(f_locals: dict) -> str:
    """
    Grabs only those dictionary items where the key contains one of the
    relevant_keywords
    """
    relevant_keywords = ["case_id", "payload", "process_id"]
    relevant_locals = {}
    for k, v in f_locals.items():
        if any([keyword in k for keyword in relevant_keywords]):
            relevant_locals[k] = v

    return ", ".join([f"{k}: {v}" for k, v in relevant_locals.items()])


def find_first_non_exception_frame(call_stack: List) -> Optional[inspect.FrameInfo]:
    """
    Returns the first non '*exception*.py' frame in the call stack.
    This should be the interesting one and is needed when we can't get the info via the
    constructor.
    """
    result = None
    for frame in call_stack:
        if "exception" not in path.basename(frame.filename):
            result = frame
            break

    return result


def get_message_from_call_stack(call_stack: List, msg: str) -> str:
    useful_frame = find_first_non_exception_frame(call_stack)
    exception_info = get_relevant_locals(f_locals=useful_frame.frame.f_locals)
    return (
        f"APIException in file: '{useful_frame.filename}', "
        f"function: {useful_frame.function}, "
        f"line: '{useful_frame.lineno}', with exception info: '{exception_info}', "
        f"message: '{msg}'"
    )


def get_rule_detail_text(rule):
    return (
        f"The rule with ID {rule.id} named {rule.name} on {rule.line_number} in "
        f"{rule.file_name}"
    )


class RuleException(Exception):
    """Generic exceptions from which all Rule-Exceptions can inherit."""

    def __init__(self, msg=None, rule_1=None, rule_2=None):
        self.message = rule_exception_message(msg=msg, rules_list=[rule_1, rule_2])


class RuleRequiresNameException(RuleException):
    """Exception raised if a rule doesn't have a human readable name"""

    def __init__(self, rule):
        if hasattr(rule, "id") and rule.id:
            self.message = (
                f"Rule on {rule.line_number} in {rule.file_name} with ID {rule.id} is "
                f"missing a name."
            )
        else:
            self.message = (
                f"There is a rule on {rule.line_number} in {rule.file_name} that is "
                f"missing a name."
            )


class RuleRequiresIdException(RuleException):
    """Exception raised if rule doesn't have an id"""

    def __init__(self, rule):
        if hasattr(rule, "name") and rule.name:
            self.message = (
                f"Rule on {rule.line_number} in {rule.file_name} with name {rule.name}"
                f" has no ID."
            )
        else:
            self.message = (
                f"There is a rule on {rule.line_number} in {rule.file_name} that has "
                f"no ID."
            )


class MethodNotAllowedException(RuleException):
    """Exception raised if a forbidden RuleauDict method is called"""

    def __init__(self, method, rule_dict):
        method_text = "delete" if method == "__delitem__" else "set"
        self.message = (
            f"A rule on {rule_dict.line_number} in {rule_dict.file_name} tried to "
            f"{method_text} a value in the dict which is not allowed."
        )


class CaseIdRequiredException(RuleException):
    """Exception raised if a json path for case identifier is not found"""

    def __init__(self, rule):
        super().__init__(
            msg=f"A case id for rule: {rule.id} was not provided which required when "
            f"posting data to the API.",
            rule_1=rule,
        )


class CannotOverrideException(Exception):
    """Exception raised if a API tries to override a rule marked as NO_OVERRIDE"""

    def __init__(self, case_id, rule):
        self.message = (
            f"Case ID {case_id} is set to override but {rule.name} on "
            f"{rule.line_number} in {rule.file_name} prohibits overrides."
        )


class DuplicateRuleNameException(RuleException):
    """Exception raised if more than 1 rule has same name"""

    def __init__(self, rule, conflict):
        # We can assume that the rule has a valid ID, given that Rule._validate()
        # will have been called from the constructor and raised an exception if it
        # wasn't.
        self.message = (
            f"The name {rule.name} on {rule.line_number} in {rule.file_name} with "
            f"id {rule.id} is in conflict with rule {conflict.id} on "
            f"{conflict.line_number} in {conflict.file_name}"
        )


class RuleIdIllegalCharacterException(RuleException):
    """Exception raise if Rule name contains illegal characters"""

    def __init__(self, rule):
        rule_detail = get_rule_detail_text(rule)
        illegal_chars = re.findall(r"[^a-zA-Z0-9-_~]", rule.id)
        self.message = (
            f"{rule_detail} has illegal characters in the ID: {illegal_chars}"
        )


class RuleFunctionNameAttributeCollisionException(RuleException):
    """If the provided rule name collides with a rule attribute"""

    def __init__(self, rule):
        self.message = (
            f"{get_rule_detail_text(rule)} in conflict with a function "
            f"with the same name."
        )


class DuplicateRuleIdException(RuleException):
    """Exception raised if more than 1 rule has same ID"""

    def __init__(self, rule, conflict):
        self.message = (
            f"{get_rule_detail_text(rule)} is in conflict with rule {conflict.id} on "
            f"{conflict.line_number} in {conflict.file_name}"
        )


class APIException(Exception):
    """Generic exception for API request failure"""

    def __init__(self, msg):
        self.message = get_message_from_call_stack(call_stack=inspect.stack(), msg=msg)


class CaseAPIException(APIException):
    def __init__(self, activity, case_id, response):
        msg = (
            f"Status Code: {response.status_code}. "
            f"Failed to {activity} case {case_id} due to {response.text}"
        )
        super().__init__(msg=msg)


class RuleAPIException(APIException):
    def __init__(self, activity, process_id, response):
        msg = (
            f"Failed to {activity} rules in process {process_id} due to "
            f"{response.text}"
        )
        super().__init__(msg=msg)


class OrganisationalDataApiException(APIException):
    def __init__(self, process_id, response):
        msg = (
            f"Failed to add the Organisational Scheme for process {process_id} due to "
            f"{response.text}"
        )
        super().__init__(msg=msg)


class UiLayoutMetadataApiException(APIException):
    def __init__(self, process_id, response):
        msg = (
            f"Failed to add the UI Layout Metadata for process {process_id} due to "
            f"{response.text}"
        )
        super().__init__(msg=msg)


class ConditionalDependencyReusedException(RuleException):
    """Exception raised if the rule has duplicate dependencies"""

    def __init__(self, rule):
        run_if_line = rule.run_if.line_number if rule.run_if is not None else "None"
        run_if_file = rule.run_if.file_name if rule.run_if is not None else "None"
        run_if_not_line = (
            rule.run_if_not.line_number if rule.run_if_not is not None else "None"
        )
        run_if_not_file = (
            rule.run_if_not.file_name if rule.run_if_not is not None else "None"
        )
        super().__init__(
            msg=(
                f"{get_rule_detail_text(rule)} "
                f" has {run_if_line}/{run_if_not_line} in "
                f"{run_if_file}/{run_if_not_file} linked as a run_if/run_if_not as a "
                f"dependency."
            ),
            rule_1=rule,
            rule_2=rule.run_if,
        )


class RuleErrorException(Exception):
    """Exception raised when a rule raises an exception"""

    def __init__(self, rule, rule_exception, case_id):
        self.rule_exception = rule_exception
        self.rule_id = rule.id
        self.rule_name = rule.name
        self.message = (
            f"{get_rule_detail_text(rule)} "
            f"has thrown an exception ({rule_exception}) with {case_id}"
        )


class RunIfRuleHasRunIfOrNotException(RuleException):
    """
    Exception raise if a run_if or run_if_not dependency of a rule also has a run_if or
    run_if_not.
    """

    def __init__(self, rule, run_if_or_not, sub_conditionals):
        self.message = (
            f"{get_rule_detail_text(rule)} has run_if/run_if_not: {run_if_or_not.id} "
            f"at {run_if_or_not.line_number} in {run_if_or_not.file_name} which is "
            f"linked to other(s) conditionals "
            f"{', '.join([sc.id for sc in sub_conditionals])} which is not a valid "
            f"state."
        )


class RunIfAndRunIfNotSameRule(RuleException):
    """The required keynames context and payload have not been provided"""

    def __init__(self, rule):
        self.rule_name = rule.name
        self.rule_id = rule.id
        self.message = (
            f"{get_rule_detail_text(rule)} has RUN_IF and RUN_IF_NOT which is linked "
            f"to the same rule which is {rule.run_if}/{rule.run_if_not}"
        )


class IncorrectKwargsForDoctests(Exception):
    """The required keynames context and payload have not been provided"""

    def __init__(self, rule):
        self.rule_id = rule.id
        self.rule_name = rule.name
        self.message = (
            f"{get_rule_detail_text(rule)} "
            f"has not been defined with the correct keyword argument names. Please "
            f"change the rule argument names to context and payload."
        )
        super().__init__(self.message)


class ImportException(Exception):
    """
    Class of exception that occurs when attempting to import
    a Ruleau ruleset for documentation
    """

    def __init__(self, module_file: str, top_level_rule: str, message: str):
        self.module_file = module_file
        self.top_level_rule = top_level_rule
        self.message = message
        super().__init__(message)


class CouldNotImportRulesToDocument(ImportException):
    """Ruleau Docs could not load the provided module and top level rule"""

    def __init__(
        self,
        module_file: str,
        top_level_rule: str,
        inner_exception: ModuleNotFoundError,
    ):
        self.inner_exception = inner_exception

        message = (
            f"Could not import the file '{module_file}' "
            f"with the top level rule '{top_level_rule}' to be documented.\n"
            f"Was unable to import a module the file depends "
            f"on called '{inner_exception.name}'"
        )

        super().__init__(module_file, top_level_rule, message)


class IncorrectTypeProvidedForImport(ImportException):
    """
    Ruleau Docs could not load the provided top level rule as it is not a Rule instance
    """

    def __init__(self, module_file: str, top_level_rule: str):

        message = (
            f"Could not import the file '{module_file}' "
            f"with the top level rule '{top_level_rule}' to be documented.\n"
            f"The provided top level rule isn't a Rule type, it must be an "
            f"instance of a rule (for example an All or Any rule)"
        )

        super().__init__(module_file, top_level_rule, message)


class DataOverrideBase(Exception):
    """Generic exceptions from which all Rule-Exceptions can inherit."""

    def __init__(self, message):
        self.message = message


class AttributeDoesntExist(DataOverrideBase):
    """Exception if the target key doesn't
    exist in the payload during a data override"""

    def __init__(self, key):
        message = f"Unable to overwrite attribute {key} as it is not in the payload"
        super().__init__(message)


class DataOverrideException(DataOverrideBase):
    """General Data Override exception"""

    def __init__(self):
        message = (
            "There was an error when applying the data"
            " override, not all overrides were completed"
        )
        super().__init__(message)


class PayloadFormatException(Exception):
    """When the payload provided is not in the correct format"""

    def __init__(self):
        super().__init__("The payload provided must be a Dict type")
