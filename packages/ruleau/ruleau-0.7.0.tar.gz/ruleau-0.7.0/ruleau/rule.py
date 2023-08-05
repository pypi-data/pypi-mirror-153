import functools
import inspect
from typing import TYPE_CHECKING, Any, AnyStr, Dict, List, Optional

import regex as re

from ruleau.constants import OverrideLevel
from ruleau.context_manager import Context
from ruleau.doc_parsers import clean_source, comments, description, doctests, parameters
from ruleau.exceptions import (
    CannotOverrideException,
    ConditionalDependencyReusedException,
    RuleErrorException,
    RuleFunctionNameAttributeCollisionException,
    RuleIdIllegalCharacterException,
    RuleRequiresIdException,
    RuleRequiresNameException,
    RunIfAndRunIfNotSameRule,
    RunIfRuleHasRunIfOrNotException,
)
from ruleau.structures import ExecutionResult, RuleauDict

if TYPE_CHECKING:
    from ruleau.adapter import ApiAdapter
    from ruleau.process import Process
    from ruleau.types import Function


class Rule:
    def __init__(
        self,
        func: "Function",
        id_: AnyStr,
        name: AnyStr,
        depends_on: List["Rule"],
        override_level: OverrideLevel = OverrideLevel.ENABLED,
        run_if: Optional["Rule"] = None,
        run_if_not: Optional["Rule"] = None,
    ):
        """
        :param func: User defined rule
        :param name: User defined human readable name of the rule
        :param depends_on: Rule dependencies
        :param override_level: Override level
        :param run_if: Optional, Conditional rule
        :param run_if_not: Optional, Conditional rule
        """
        self.id = id_
        self.name = name
        # Set the user defined function
        self.func = func

        # Set exception debug information
        info = self._get_relevant_call_stack_info()
        self.line_number = info["lineno"]
        self.file_name = info["filename"]

        # Validate the rule, make sure the name is always set for a rule
        self._validate()

        # Set the override level for rule
        self.override_level = override_level
        # Set rule function name
        self.__name__ = func.__name__

        # Setup the rule dependencies
        self.depends_on = depends_on
        self.run_if = run_if
        self.run_if_not = run_if_not

        # Set default values for order & result
        self.order = None
        self.execution_result = None

        # Validate dependencies
        self._validate_duplicate_dependencies()
        self._validate_run_if_or_if_not()

        # This preserves the original Docstring on the decorated function
        # which allows DocTest to detect the function
        functools.update_wrapper(self, func)

    @property
    def dependencies(self):

        if self.run_if and self.run_if_not:
            return self.depends_on + [self.run_if, self.run_if_not]
        if self.run_if:
            return self.depends_on + [self.run_if]
        if self.run_if_not:
            return self.depends_on + [self.run_if_not]

        return self.depends_on

    def __str__(self) -> str:
        return f"{str(self.id)} - {str(self.name)} ({str(self.__name__)})"

    def __repr__(self):
        return str(self)

    def __call__(self, *args, **kwargs) -> bool:
        return self.func(*args, **kwargs)

    @staticmethod
    def _get_relevant_call_stack_info():
        found_rule_py = False
        result = {"lineno": -1, "filename": ""}
        current_frame = inspect.currentframe()
        while current_frame:
            filename = current_frame.f_code.co_filename
            if (
                filename.endswith("rule.py")
                and current_frame.f_code.co_name == "__init__"
            ):
                found_rule_py = True
            elif found_rule_py and "decorators.py" not in filename:
                result["filename"] = filename
                result["lineno"] = current_frame.f_lineno
                break
            current_frame = current_frame.f_back
        return result

    def _validate(self):
        """
        Validator to check if top level rule has a human readable name
        and id
        :raises: TopLevelRuleRequiresNameException
        :raises: RuleRequiresIdException
        """
        # Validate if Rule name is present
        if not self.name or not isinstance(self.name, str):
            raise RuleRequiresNameException(rule=self)

        # Validate if Rule ID is present
        if not self.id or not isinstance(self.id, str):
            raise RuleRequiresIdException(rule=self)

        # Validate the Rule ID
        if not re.match(r"^([a-zA-Z0-9-_~]+)+$", self.id):
            raise RuleIdIllegalCharacterException(rule=self)

        # If an attribute with the same name as the function name
        try:
            getattr(self, self.func.__name__)
            raise RuleFunctionNameAttributeCollisionException(rule=self)
        except AttributeError:
            pass

    def _validate_duplicate_dependencies(self):
        """
        Validator to check if rule has duplicate dependencies
        in run_if and depends_on
        :raises: ConditionalDependencyReusedException
        """
        if (self.run_if and self.run_if_not) and (self.run_if == self.run_if_not):
            raise RunIfAndRunIfNotSameRule(self)

        # Validate if there are no duplicate dependencies
        for rule_depends in [self.run_if, self.run_if_not]:
            if rule_depends and rule_depends in self.depends_on:
                raise ConditionalDependencyReusedException(rule=self)

    def _validate_run_if_or_if_not(self):
        conditionals = Rule._get_conditionals(self)
        if conditionals:
            for cond in conditionals:
                if sub_cons := Rule._get_conditionals(cond):
                    raise RunIfRuleHasRunIfOrNotException(
                        rule=self, run_if_or_not=cond, sub_conditionals=sub_cons
                    )

    def _get_source(self) -> AnyStr:
        """Get the cleaned source code of the rule"""
        return clean_source(inspect.getsource(self.func))

    @staticmethod
    def _get_conditionals(current_rule):
        if current_rule is None:
            return []
        results = []
        if current_rule.run_if:
            results.append(current_rule.run_if)
        if current_rule.run_if_not:
            results.append(current_rule.run_if)
        return results

    @property
    def description(self) -> AnyStr:
        """Parse the description of rule"""
        return description(self.func.__doc__)

    def calculate_order_values(self, index=None):
        """
        This sets the `order` value for this rule
        and all of the dependencies below it.

        :param index: Used internally, do not set
        """
        if index is None:
            self.order = 0
        else:
            if self.order is not None:
                self.order = max(self.order, index + 1)
            else:
                self.order = index + 1
        for dependency in self.dependencies:
            dependency.calculate_order_values(self.order)

    def flatten_rule_objects(self, flat_rules=None) -> List["Rule"]:
        """Method to flatten rule objects, usually used for root rule"""
        if flat_rules is None:
            flat_rules = []
        flat_rules.append(self)
        for dependency in self.dependencies:
            dependency.flatten_rule_objects(flat_rules)
        return flat_rules

    def parse(self):
        """Collects and returns parsed rule data for documentation
        :return: Dictionary of rule data
        """
        return {
            "id": self.id,
            "name": self.name,
            "rule_type": type(self).__name__,
            "order": self.order,
            "override_level_name": self.override_level.name,
            "override_level": self.override_level.value,
            "source": self._get_source(),
            "comments": comments(self._get_source()),
            "docstring": self.func.__doc__,
            "description": self.description,
            "parameters": parameters(self.func.__doc__),
            "dependencies": self.sort_dependencies(),
            "depends_on": [],
            "doctests": doctests(self.func),
        }

    def sort_dependencies(self):
        """
        Sort the dependencies so that those with conditional rules come first.
        Returns a list of dicts suitable for display.
        """
        return sorted(
            [
                {
                    "id": dependent.id,
                    "run_if": dependent == self.run_if,
                    "run_if_not": dependent == self.run_if_not,
                }
                for dependent in self.dependencies
            ],
            key=lambda d: d["run_if"] or d["run_if_not"],
            reverse=True,
        )

    def execute(
        self,
        case_id: AnyStr,
        payload: Dict[AnyStr, Any],
        process: "Process",
        api_adapter: Optional["ApiAdapter"] = None,
        rule_overrides: Optional[Dict] = None,
    ) -> ExecutionResult:
        """
        Execute the rule and apply overrides
        :param case_id: Case ID
        :param payload: Case payload
        :param process: Process instance
        :param api_adapter: ApiAdapter instance
        :param rule_overrides: Overrides dictionary
        :return: ExecutionResult of the rule
        """

        # Test the results of run_if rules
        run_if_result = True
        if self.run_if:
            run_if_result = self.run_if.execute(
                case_id=case_id,
                payload=payload,
                process=process,
                api_adapter=api_adapter,
                rule_overrides=rule_overrides,
            ).result

        if self.run_if_not:
            result = self.run_if_not.execute(
                case_id=case_id,
                payload=payload,
                process=process,
                api_adapter=api_adapter,
                rule_overrides=rule_overrides,
            ).result
            run_if_result = (not result) and run_if_result

        # if it fails then skip the execution of this rule
        if not run_if_result:
            self.skip_execution()
            self.remove_stale_data()
            return self.execution_result

        # If the rule is already executed return the previous result
        # unless that result was skipped
        if (
            self.execution_result
            and not self.execution_result.skipped
            and payload == self.execution_result.payload
        ):
            return self.execution_result

        # Prep the rule payload
        rule_payload = RuleauDict(payload)

        # Run this rule dependencies
        dependency_results = {
            dependency: dependency.execute(
                case_id=case_id,
                payload=payload,
                process=process,
                api_adapter=api_adapter,
                rule_overrides=rule_overrides,
            )
            for dependency in self.depends_on
        }
        context = Context(dependency_results)

        self.execution_result = ExecutionResult(
            self,
            rule_payload,
            None,
            dependency_results,
        )

        # Run this rule
        try:
            rule_result = self.__call__(context, rule_payload)
            self.execution_result.result = rule_result
        # If it fails mark it as failed
        except Exception as e:
            self.skip_execution()
            self.execution_result.failed = True
            raise RuleErrorException(rule=self, rule_exception=e, case_id=case_id)

        if api_adapter:
            # Apply overrides on the rule result
            self.execution_result = self.apply_override(
                case_id, process, self.execution_result, rule_overrides
            )

        # Assign to internal object & return the rule result
        return self.execution_result

    def apply_override(
        self,
        case_id,
        process,
        execution_result: ExecutionResult,
        rule_overrides: Dict,
    ) -> ExecutionResult:
        """
        Check if there are any overrides to apply to this case. If so apply the
        override.
        :param case_id: Case ID
        :param execution_result: ExecutionResult of a rule
        :param rule_overrides: Dictionary of all rule overrides
        :return: ExecutionResult of the rule
        """
        # Get overrides for the rule in a case
        key = tuple([case_id, process.id, self.id])
        override = (
            rule_overrides[key] if rule_overrides and key in rule_overrides else None
        )

        # Apply override to the executed rule result, if any
        # Overrides should only be applied to allowed rule and if they're present
        if override:
            # Throw an exception if the backend is trying to override a DISABLED rule
            if self.override_level == OverrideLevel.DISABLED:
                raise CannotOverrideException(case_id=case_id, rule=self)
            else:
                # Override the rule result and set the overridden flag
                execution_result.override = override["id"]
                execution_result.original_result = execution_result.result
                execution_result.result = override["applied"]
        return execution_result

    def skip_execution(self):
        """
        Recursively skip a rule and all its children. If a rule is skipped when
        it already has a result, that result is kept.
        """
        if self.execution_result is None:
            self.execution_result = ExecutionResult.skipped_result(self)
        for dependency in self.depends_on:
            dependency.skip_execution()

    def remove_stale_data(self):
        """
        Recursively removes stale data from nested Rules
        """

        self.execution_result.failed = False
        self.execution_result.original_result = None
        self.execution_result.override = None
        self.execution_result.payload = None
        self.execution_result.result = None
        self.execution_result.skipped = True

        for dependency in self.depends_on:
            dependency.remove_stale_data()
