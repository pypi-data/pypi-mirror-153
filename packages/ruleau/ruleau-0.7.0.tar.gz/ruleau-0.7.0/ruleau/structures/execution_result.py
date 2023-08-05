from typing import TYPE_CHECKING, AnyStr, Dict, List, Optional

if TYPE_CHECKING:
    from ruleau.rule import Rule
    from ruleau.structures import RuleauDict


class ExecutionResult:
    def __init__(
        self,
        executed_rule: "Rule",
        payload: "RuleauDict",
        result,
        dependent_results: Dict["Rule", "ExecutionResult"],
        override: AnyStr = None,
        original_result: Optional[bool] = None,
        skipped: bool = False,
        failed: bool = False,
    ):
        self.rule = executed_rule
        self.payload = payload
        self.result = result
        self.override = override
        self.original_result = original_result
        self.dependent_results = dependent_results
        self.skipped = skipped
        self.failed = failed

    @property
    def rule_results(self) -> List["ExecutionResult"]:
        """Returns flat list of ExecutionResults for this rule and
        all descendants of this rule"""
        return self._flatten_rule_results()

    def _flatten_rule_results(self, flat_rule_results=None) -> List["ExecutionResult"]:
        if flat_rule_results is None:
            flat_rule_results = []
        if self not in flat_rule_results:
            flat_rule_results.append(self)
        for execution_result in self.dependent_results.values():
            execution_result._flatten_rule_results(flat_rule_results)
        return flat_rule_results

    @staticmethod
    def skipped_result(rule: "Rule") -> "ExecutionResult":
        """Creates an ExecutionResult for a skipped rule"""
        return ExecutionResult(rule, None, None, {}, skipped=True)
