from rule_based_block_rules import account_status
from ruleau import Process, execute

if __name__ == "__main__":
    execution_result = execute(
        account_status,
        {
            "loc_record": {
                "loc_number": 12345,
                "current_dnp": 0,
                "current_cons_full_pmt": 4,
                "expected_payments_passed": 1,
                "expected_payments_future": 15,
                "total_pending_payment": 1234.51,
                "total_balance": 2345.21,
                "principal_balance": 1995.85,
                "plaid_active_flag": True,
                "draw": [
                    {
                        "draw_date": "2019-01-01T00:00:00.000Z",
                        "amount": 5000.01,
                        "principal_post_draw": 8123.50,
                    },
                    {
                        "draw_date": "2019-06-01T00:00:00.000Z",
                        "amount": 4000.02,
                        "principal_post_draw": 5123.50,
                    },
                ],
                "missed_pmt": [
                    {
                        "missed_pmt_cluster": 1,
                        "payment_date": "2021-01-01T00:00:00.000Z",
                    },
                    {
                        "missed_pmt_cluster": 1,
                        "payment_date": "2020-12-26T00:00:00.000Z",
                    },
                    {
                        "missed_pmt_cluster": 2,
                        "payment_date": "2020-11-01T00:00:00.000Z",
                    },
                ],
                "modification": [
                    {
                        "applied": "2020-01-01T00:00:00.000Z",
                        "suspended": "2020-02-01T00:00:00.000Z",
                        "mod_cluster": 1,
                        "reduction_perc": 50,
                        "instalment_amount": 200.05,
                    },
                    {
                        "applied": "2020-02-01T00:00:00.000Z",
                        "suspended": "2020-02-05T00:00:00.000Z",
                        "mod_cluster": 1,
                        "reduction_perc": 100,
                        "instalment_amount": 0,
                    },
                    {
                        "applied": "2020-03-01T00:00:00.000Z",
                        "suspended": "2020-01-01T00:00:00.000Z",
                        "mod_cluster": 2,
                        "reduction_perc": 75,
                        "instalment_amount": 100.03,
                    },
                ],
            }
        },
        Process.create_process_from_rule(account_status),
    )

    for rule_result in execution_result.rule_results:
        print(
            "{0} - {1} - {2}".format(
                rule_result.rule.id.ljust(20),
                str(rule_result.result).ljust(5),
                rule_result.rule.name,
            )
        )
