from typing import AnyStr, Optional

from ruleau.constants import OverrideLevel
from ruleau.rule import Rule
from ruleau.structures import ExecutionResult


class Any(Rule):
    """Aggregator to implement OR operation
    Returns truthy, if any one of the rule result is truthy
    """

    def __init__(
        self,
        rule_id: AnyStr,
        name: AnyStr,
        *rules: "Rule",
        description: AnyStr = None,
        override_level: OverrideLevel = OverrideLevel.ENABLED,
        run_if: Optional[Rule] = None,
        run_if_not: Optional[Rule] = None,
    ):
        def any_aggregator(context: ExecutionResult, _):
            if all([result.skipped for result in context.dependent_results]):
                self.skip_execution()
                self.remove_stale_data()
                return None
            return any(result.result for result in context.dependent_results)

        any_aggregator.__doc__ = description if description else Any.__doc__
        super().__init__(
            any_aggregator,
            rule_id,
            name,
            list(rules),
            override_level,
            run_if,
            run_if_not,
        )


class All(Rule):
    """Aggregator to implement AND operation
    Returns truthy, if all of the rule results are truthy
    """

    def __init__(
        self,
        rule_id: AnyStr,
        name: AnyStr,
        *rules: "Rule",
        description: AnyStr = None,
        override_level: OverrideLevel = OverrideLevel.ENABLED,
        run_if: Optional[Rule] = None,
        run_if_not: Optional[Rule] = None,
    ):
        def all_aggregator(context: ExecutionResult, _):
            if all([result.skipped for result in context.dependent_results]):
                self.skip_execution()
                self.remove_stale_data()
                return None
            return all(
                result.result
                for result in context.dependent_results
                if not result.skipped
            )

        all_aggregator.__doc__ = description if description else All.__doc__
        super().__init__(
            all_aggregator,
            rule_id,
            name,
            list(rules),
            override_level,
            run_if,
            run_if_not,
        )


class AllFail(Rule):
    """Aggregator to implement NONE/Not Any/All Fail/None shall pass operation
    Returns true, if all of the rule results are false
    """

    def __init__(
        self,
        rule_id: AnyStr,
        name: AnyStr,
        *rules: "Rule",
        description: AnyStr = None,
        override_level: OverrideLevel = OverrideLevel.ENABLED,
        run_if: Optional[Rule] = None,
        run_if_not: Optional[Rule] = None,
    ):
        def all_fail_aggregator(context: ExecutionResult, _):
            if all([result.skipped for result in context.dependent_results]):
                self.skip_execution()
                self.remove_stale_data()
                return None
            return all(
                result.result is False
                for result in context.dependent_results
                if not result.skipped
            )

        all_fail_aggregator.__doc__ = description if description else AllFail.__doc__
        super().__init__(
            all_fail_aggregator,
            rule_id,
            name,
            list(rules),
            override_level,
            run_if,
            run_if_not,
        )
