import json
from typing import TYPE_CHECKING, AnyStr, Dict

from ruleau.structures import ExecutionResult

if TYPE_CHECKING:
    from ruleau.rule import Rule


class Context:
    """
    The context is passed in to the execution of a rule. It stores the results
    of the dependencies of the rule.
    """

    class DependentResults:
        """
        Used primarily to support iterating through all the results using
        `for result in context.dependent_results` in a rule
        """

        def __init__(self, execution_results: Dict["Rule", "ExecutionResult"]):
            self.dependencies = execution_results

        def _get_execution_result(self, rule):
            try:
                return self.dependencies[rule]
            except KeyError as e:
                # Although it would be nice to share the function name, that's
                # not necessarily available to us (e.g. if the rule is created)
                # using a factory function such as the agreggators
                raise AttributeError(
                    f"Result for rule '{rule}' not available, as it was not "
                    f"declared as a dependency'. "
                    f"Update the `depends_on` attribute of this rule to include"
                    f"the required object (currently depending on rule ids "
                    f"{json.dumps(list(rule.id for rule in self.dependencies.keys()))}"
                    f" )",
                    e,
                )

        def __iter__(self):
            # Iterate through the dependencies
            for dep in self.dependencies:
                yield self._get_execution_result(dep)

    def __init__(self, execution_results: Dict["Rule", "ExecutionResult"]):
        self.execution_results = execution_results
        self.dependent_results = self.DependentResults(execution_results)

    def _get_execution_result(self, rule):
        return self.dependent_results._get_execution_result(rule)

    def get_result(self, rule):
        return self._get_execution_result(rule).result


def mock_context(rule_results: Dict[str, bool]):
    """
    Given an dictionary containing the rule function name
    as the key and the mocked result as the value, creates
    an ExecutionResult.

    :param rule_results: A dictionary containing the mock
    results for the depedent rules

    :return: ExecutionResult containing mocked results
    """

    class MockDependentResults(Context.DependentResults):
        def _get_execution_result(self, rule):
            return self.dependencies[rule.__name__]

    class MockContext(Context):
        def __init__(self, execution_results):
            self.execution_results = execution_results
            self.dependent_results = MockDependentResults(execution_results)

    return MockContext(
        {
            key: ExecutionResult(None, {}, value, {})
            for key, value in rule_results.items()
        }
    )
