from lending_rules import (
    ccjs_check_required,
    fico_score_greater_than_threshold,
    has_no_ccjs,
    has_sufficient_capital,
    kyc_risk_greater_than_threshold,
)

from ruleau import All, ApiAdapter, Process, execute, rule


@rule("rul-101A", "Causes skipped")
def causes_skip(_, __):
    return False


@rule("rul_101", "Skipped Rule", run_if=causes_skip)
def skipped_rule(_, __):
    return False


@rule("rul-102A", "Causes not skipped")
def causes_no_skip(_, __):
    return True


@rule("rul_102", "Not Skipped Rule", run_if=causes_no_skip)
def not_skipped_rule(_, __):
    return False


@rule("rul200-c", "Skipped tree bottom")
def skipped_tree_bottom(_, __):
    return False


@rule(
    "rul200-a",
    "Skipped tree 1  skipped",
    depends_on=[skipped_tree_bottom],
    run_if=causes_skip,
)
def skipped_tree_1_a(_, __):
    return False


@rule(
    "rul200-b",
    "Skipped tree 1 not skipped",
    depends_on=[skipped_tree_bottom],
    run_if=causes_no_skip,
)
def skipped_tree_1_b(_, __):
    return False


@rule("rul200", "Skipped tree 1 Top", depends_on=[skipped_tree_1_a, skipped_tree_1_b])
def skipped_tree_1(_, __):
    return False


conditionals = All(
    "ID",
    "name",
    skipped_rule,
    causes_no_skip,
    skipped_tree_1,
)

will_lend = All(
    "WL_01",
    "Will Lend",
    kyc_risk_greater_than_threshold,
    fico_score_greater_than_threshold,
    has_no_ccjs,
    has_sufficient_capital,
    conditionals,
)

if __name__ == "__main__":
    api_adapter = ApiAdapter(base_url="http://127.0.0.1:8000")
    process = Process.create_process_from_rule(will_lend)
    api_adapter.sync_process(process)
    result = execute(
        will_lend,
        {
            "data": {
                "fico_score": 150,
                "ccjs": [],
                "kyc": "low",
                "number_of_children": 1,
                "capital": 10_000,
                "ccjs_required": True,
            }
        },
        process,
        api_adapter=api_adapter,
        case_id="132",
    )
    print("Result", result.result)
