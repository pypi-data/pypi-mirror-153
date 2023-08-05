from collections import OrderedDict
from typing import TYPE_CHECKING, Any, AnyStr, Dict, Optional

from ruleau.exceptions import RuleErrorException
from ruleau.rule import Rule
from ruleau.structures import ErrorMessage

if TYPE_CHECKING:
    from ruleau.adapter import ApiAdapter


class Process:
    """Class holding rule process"""

    error: Optional[ErrorMessage]

    def __init__(
        self,
        process_id: str,
        name: str,
        description: str,
        root_rule: Rule,
    ):
        self.id = process_id
        self.name = name
        self.description = description
        self.root_rule = root_rule
        self.error = None
        self.data_override_changes = None
        self.rule_overrides = None

    @staticmethod
    def create_process_from_rule(rule: Rule) -> "Process":
        return Process(
            process_id=rule.id,
            name=rule.name,
            description=rule.description,
            root_rule=rule,
        )

    @property
    def rules(self):
        return list(OrderedDict.fromkeys(self.root_rule.flatten_rule_objects()))

    def parse(self):
        self.root_rule.calculate_order_values()

        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "root_rule": self.root_rule.id,
            "rules": [rule.parse() for rule in self.rules],
        }

    def execute(
        self,
        case_id: AnyStr,
        payload: Dict[AnyStr, Any],
        api_adapter: Optional["ApiAdapter"] = None,
        data_override_changes: Dict = None,
        rule_overrides: Dict = None,
        setup_error: Optional[ErrorMessage] = None,
    ):
        self.data_override_changes = data_override_changes
        self.rule_overrides = rule_overrides
        self.error = setup_error

        try:

            result = None

            if self.error:
                self.root_rule.skip_execution()
                result = False
            else:
                result = self.root_rule.execute(
                    case_id=case_id,
                    payload=payload,
                    process=self,
                    api_adapter=api_adapter,
                    rule_overrides=self.rule_overrides,
                )
            return result

        # If any exception is hit during the process execution
        except RuleErrorException as e:
            message = e.message

            self.error = {"error_name": e.__class__.__name__, "error_message": message}
            raise e.rule_exception
        finally:
            # Always sync the rules current state
            if api_adapter:
                api_adapter.sync_results(self, case_id)
