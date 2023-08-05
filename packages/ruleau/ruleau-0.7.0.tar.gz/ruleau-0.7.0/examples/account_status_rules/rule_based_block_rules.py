from datetime import datetime, timedelta

from ruleau import All, rule


@rule(rule_id="MP-001-B1", name="Days Not Paid")
def days_not_paid(_, payload):
    """
    Block if the latest payment is now late (i.e. Days not paid is greater than zero).

    >>> days_not_paid(None, {"loc_record": {"current_dnp": 1}})
    False
    >>> days_not_paid(None, {"loc_record": {"current_dnp": 0}})
    True
    """
    # Fail if days not paid is greater than zero.
    return payload["loc_record"]["current_dnp"] == 0


@rule(rule_id="MP-001-U1", name="Two Consecutive Payments Made")
def two_consecutive_payments_made(_, payload):
    """
    Unblock if two consecutive, non-reduced payments been made.
    :Override Guidance: Testing out override guidance param.

    >>> two_consecutive_payments_made(None, {"loc_record": {"current_cons_full_pmt": 1, "expected_payments_passed": 10}})
    False
    >>> two_consecutive_payments_made(None, {"loc_record": {"current_cons_full_pmt": 2, "expected_payments_passed": 10}})
    True
    >>> two_consecutive_payments_made(None, {"loc_record": {"current_cons_full_pmt": 0, "expected_payments_passed": 1}})
    False
    >>> two_consecutive_payments_made(None, {"loc_record": {"current_cons_full_pmt": 1, "expected_payments_passed": 1}})
    True
    """
    # Default the required number of consecutive payments to two.
    consecutive_payment_required = 2

    # If the account is new (and so can not yet meet the required number of consecutive payments) then lower the number required.
    if payload["loc_record"]["expected_payments_passed"] < consecutive_payment_required:
        consecutive_payment_required = payload["loc_record"]["expected_payments_passed"]

    # Fail if the current number of consecutive full payments is less than the required number of payments.
    return (
        payload["loc_record"]["current_cons_full_pmt"] >= consecutive_payment_required
    )


@rule(rule_id="MP-002-B1", name="Two Missed Payments in 90 Days")
def two_missed_payments(_, payload):
    """
    Block if there are missed two payments within the last 90 days.

    :Override Guidance: Test guidance


    >>> two_missed_payments(None, {"loc_record": {"missed_pmt": [
    ...            {
    ...                "missed_pmt_cluster": 1,
    ...                "payment_date": "2021-02-01T09:00:00.000Z"
    ...            },
    ...            {
    ...                "missed_pmt_cluster": 1,
    ...                "payment_date": "2021-01-01T12:00:00.000Z"
    ...            },
    ...            {
    ...                "missed_pmt_cluster": 2,
    ...                "payment_date": "2020-11-01T00:00:00.000Z"
    ...            }
    ...        ]}})
    True
    """

    # Identify all the missed payments within the last 90 days
    missed_payments_list = []
    for missed_pmt in payload["loc_record"]["missed_pmt"]:
        if datetime.strptime(missed_pmt["payment_date"], "%Y-%m-%dT%H:%M:%S.%fZ") >= (
            datetime.today() - timedelta(days=90)
        ):
            missed_payments_list.append(missed_pmt)

    # Fail if the number of missed payments identified is 2 or more.
    return len(missed_payments_list) < 2


@rule(rule_id="MP-002-U1", name="Three Consecutive Payments Made")
def three_consecutive_payments_made(_, payload):
    """
    Unblock if three consecutive, non-reduced payments have been made.

    >>> three_consecutive_payments_made(None, {"loc_record": {"current_cons_full_pmt": 2, "expected_payments_passed": 10}})
    False
    >>> three_consecutive_payments_made(None, {"loc_record": {"current_cons_full_pmt": 3, "expected_payments_passed": 10}})
    True
    >>> three_consecutive_payments_made(None, {"loc_record": {"current_cons_full_pmt": 0, "expected_payments_passed": 1}})
    False
    >>> three_consecutive_payments_made(None, {"loc_record": {"current_cons_full_pmt": 2, "expected_payments_passed": 2}})
    True
    """
    # Default the required number of consecutive payments to three.
    consecutive_payment_required = 3

    # If the account is new (and so can not yet meet the required number of consecutive payments) then lower the number required.
    if payload["loc_record"]["expected_payments_passed"] < consecutive_payment_required:
        consecutive_payment_required = payload["loc_record"]["expected_payments_passed"]

    # Fail if the current number of consecutive full payments is less than the required number of payments.
    return (
        payload["loc_record"]["current_cons_full_pmt"] >= consecutive_payment_required
    )


@rule(rule_id="MP-003-B1", name="Three Missed Payments in 90 Days")
def three_missed_payments(_, payload):
    """
    Block if there are three missed payments within the last 90 days.

    >>> three_missed_payments(None, {"loc_record": {"missed_pmt": [
    ...            {
    ...                "missed_pmt_cluster": 1,
    ...                "payment_date": "2021-08-01T09:00:00.000Z"
    ...            },
    ...            {
    ...                "missed_pmt_cluster": 1,
    ...                "payment_date": "2021-07-25T12:00:00.000Z"
    ...            },
    ...            {
    ...                "missed_pmt_cluster": 1,
    ...                "payment_date": "2021-07-18T00:00:00.000Z"
    ...            }
    ...        ]}})
    False
    >>> three_missed_payments(None, {"loc_record": {"missed_pmt": [
    ...            {
    ...                "missed_pmt_cluster": 1,
    ...                "payment_date": "2021-08-01T09:00:00.000Z"
    ...            },
    ...            {
    ...                "missed_pmt_cluster": 1,
    ...                "payment_date": "2021-07-01T12:00:00.000Z"
    ...            },
    ...            {
    ...                "missed_pmt_cluster": 2,
    ...                "payment_date": "2020-02-01T00:00:00.000Z"
    ...            }
    ...        ]}})
    True
    """

    # Identify all missed payments within the last 90 days.
    missed_payments_list = []
    for missed_pmt in payload["loc_record"]["missed_pmt"]:
        if datetime.strptime(missed_pmt["payment_date"], "%Y-%m-%dT%H:%M:%S.%fZ") >= (
            datetime.today() - timedelta(days=90)
        ):
            missed_payments_list.append(missed_pmt)

    # Fail if the number of missed payments identified is 3 or more.
    return len(missed_payments_list) < 3


@rule(rule_id="MP-003-U1", name="Four Consecutive Payments Made")
def four_consecutive_payments_made(_, payload):
    """
    Unblock if four consecutive, non-reduced payments have been made.

    >>> four_consecutive_payments_made(None, {"loc_record": {"current_cons_full_pmt": 3, "expected_payments_passed": 10}})
    False
    >>> four_consecutive_payments_made(None, {"loc_record": {"current_cons_full_pmt": 4, "expected_payments_passed": 10}})
    True
    >>> four_consecutive_payments_made(None, {"loc_record": {"current_cons_full_pmt": 2, "expected_payments_passed": 3}})
    False
    >>> four_consecutive_payments_made(None, {"loc_record": {"current_cons_full_pmt": 3, "expected_payments_passed": 3}})
    True
    """
    # Default the required number of consecutive payments to four.
    consecutive_payment_required = 4

    # If the account is new (and so can not yet meet the required number of consecutive payments) then lower the number required.
    if payload["loc_record"]["expected_payments_passed"] < consecutive_payment_required:
        consecutive_payment_required = payload["loc_record"]["expected_payments_passed"]

    # Fail if the current number of consecutive full payments is less than the required number of payments.
    return (
        payload["loc_record"]["current_cons_full_pmt"] >= consecutive_payment_required
    )


@rule(rule_id="MP-004-B1", name="More Than Three Missed Payments in 90 Days")
def more_than_three_missed_payments(_, payload):
    """
    Block if there are more than three missed payments within the last 90 days.


    >>> more_than_three_missed_payments(None, {"loc_record": {"missed_pmt": [
    ...            {
    ...                "missed_pmt_cluster": 1,
    ...                "payment_date": "2021-08-01T09:00:00.000Z"
    ...            },
    ...            {
    ...                "missed_pmt_cluster": 1,
    ...                "payment_date": "2021-07-25T12:00:00.000Z"
    ...            },
    ...            {
    ...                "missed_pmt_cluster": 2,
    ...                "payment_date": "2021-07-07T08:00:00.456Z"
    ...            },
    ...            {
    ...                "missed_pmt_cluster": 2,
    ...                "payment_date": "2021-06-30T15:45:15.000Z"
    ...            },
    ...            {
    ...                "missed_pmt_cluster": 3,
    ...                "payment_date": "2021-02-01T18:00:12.123Z"
    ...            }
    ...        ]}})
    False
    >>> more_than_three_missed_payments(None, {"loc_record": {"missed_pmt": [
    ...            {
    ...                "missed_pmt_cluster": 1,
    ...                "payment_date": "2021-08-08T09:00:00.000Z"
    ...            },
    ...            {
    ...                "missed_pmt_cluster": 1,
    ...                "payment_date": "2021-08-01T12:00:00.000Z"
    ...            },
    ...            {
    ...                "missed_pmt_cluster": 1,
    ...                "payment_date": "2021-07-25T15:00:00.000Z"
    ...            },
    ...            {
    ...                "missed_pmt_cluster": 2,
    ...                "payment_date": "2020-11-01T00:00:00.000Z"
    ...            }
    ...        ]}})
    True
    """

    # Identify all missed payments within the last 90 days.
    missed_payments_list = []
    for missed_pmt in payload["loc_record"]["missed_pmt"]:
        if datetime.strptime(missed_pmt["payment_date"], "%Y-%m-%dT%H:%M:%S.%fZ") >= (
            datetime.today() - timedelta(days=90)
        ):
            missed_payments_list.append(missed_pmt)

    # Fail if the number of missed payments identified is greater three.
    return len(missed_payments_list) < 4


@rule(rule_id="MP-004-U1", name="Six Consecutive Payments Made")
def six_consecutive_payments_made(_, payload):
    """
    Unblock if six consecutive, non-reduced payments have been made.

    >>> six_consecutive_payments_made(None, {"loc_record": {"current_cons_full_pmt": 6, "expected_payments_passed": 10}})
    True
    >>> six_consecutive_payments_made(None, {"loc_record": {"current_cons_full_pmt": 5, "expected_payments_passed": 10}})
    False
    >>> six_consecutive_payments_made(None, {"loc_record": {"current_cons_full_pmt": 5, "expected_payments_passed": 5}})
    True
    >>> six_consecutive_payments_made(None, {"loc_record": {"current_cons_full_pmt": 4, "expected_payments_passed": 5}})
    False
    """
    # Default the required number of consecutive payments to three.
    consecutive_payment_required = 6

    # If the account is new (and so can not yet meet the required number of consecutive payments) then lower the number required.
    if payload["loc_record"]["expected_payments_passed"] < consecutive_payment_required:
        consecutive_payment_required = payload["loc_record"]["expected_payments_passed"]

    # Fail if the current number of consecutive full payments is less than the required number of payments.
    return (
        payload["loc_record"]["current_cons_full_pmt"] >= consecutive_payment_required
    )


@rule(rule_id="PR-001-B1", name="Two Payment Reductions in 180 Days")
def two_payment_reductions_in_180_days(_, payload):
    """
    Block if there are two or more payment reductions within the last 180 days.

    >>> two_payment_reductions_in_180_days(None, {"loc_record": {
    ...         "modification": [
    ...             {
    ...                 "applied": "2021-07-01T00:00:00.000Z",
    ...                 "reduction_perc": 50
    ...             },
    ...             {
    ...                 "applied": "2021-06-01T00:00:00.000Z",
    ...                 "reduction_perc": 75
    ...             },
    ...         ]
    ...     }})
    True
    >>> two_payment_reductions_in_180_days(None, {"loc_record": {
    ...         "modification": [
    ...             {
    ...                 "applied": "2021-07-01T00:00:00.000Z",
    ...                 "reduction_perc": 50
    ...             },
    ...             {
    ...                 "applied": "2021-01-01T00:00:00.000Z",
    ...                 "reduction_perc": 75
    ...             },
    ...         ]
    ...     }})
    False
    """

    # Identify all the payment reductions applied within the last 180 days.
    payment_reductions_list = [
        x
        for x in payload["loc_record"]["modification"]
        if datetime.strptime(x["applied"], "%Y-%m-%dT%H:%M:%S.%fZ")
        >= (datetime.today() - timedelta(days=180))
        if x["reduction_perc"] > 0
    ]

    # Fail if 2 or more reductions were identified.
    return len(payment_reductions_list) >= 2


@rule(rule_id="PR-001-U1", name="50% of Principal Paid")
def fifty_percent_principal_paid(_, payload):
    """
    Unblock if 50% of the principal balance has been paid following the most recent payment.

    >>> fifty_percent_principal_paid(None, {"loc_record": {
    ...         "principal_balance": 5000,
    ...         "draw": [
    ...             {
    ...                 "draw_date": "2021-08-01T00:00:00.000Z",
    ...                 "amount": 3000.00,
    ...                 "principal_post_draw": 12000.00
    ...             },
    ...             {
    ...                 "draw_date": "2019-07-01T00:00:00.000Z",
    ...                 "amount": 2000.00,
    ...                 "principal_post_draw": 15000.00
    ...             }
    ...         ]
    ...     }})
    True
    >>> fifty_percent_principal_paid(None, {"loc_record": {
    ...         "principal_balance": 8000,
    ...         "draw": [
    ...             {
    ...                 "draw_date": "2021-08-01T00:00:00.000Z",
    ...                 "amount": 3000.00,
    ...                 "principal_post_draw": 12000.00
    ...             },
    ...             {
    ...                 "draw_date": "2019-07-01T00:00:00.000Z",
    ...                 "amount": 2000.00,
    ...                 "principal_post_draw": 15000.00
    ...             }
    ...         ]
    ...     }})
    False
    """
    # Calculate the required balance threshold (i.e. 50% of the actual balance following the latest draw).
    balance_threshold = 0
    if len(payload["loc_record"]["draw"]) > 0:
        balance_threshold = (
            payload["loc_record"]["draw"][0]["principal_post_draw"] * 0.5
        )

    # Fail if balance required is greater than the account principal balance.
    return payload["loc_record"]["principal_balance"] <= balance_threshold


@rule(rule_id="PR-002-B1", name="Two Payment Reductions in 90 Days")
def two_payment_reductions_in_90_days(_, payload):
    """
    Block if there are two or more payment reductions within the last 90 days.

    >>> two_payment_reductions_in_90_days(None, {"loc_record": {
    ...         "modification": [
    ...             {
    ...                 "applied": "2021-08-01T00:00:00.000Z",
    ...                 "reduction_perc": 50
    ...             },
    ...             {
    ...                 "applied": "2021-07-25T00:00:00.000Z",
    ...                 "reduction_perc": 75
    ...             },
    ...         ]
    ...     }})
    True
    >>> two_payment_reductions_in_90_days(None, {"loc_record": {
    ...         "modification": [
    ...             {
    ...                 "applied": "2021-07-01T00:00:00.000Z",
    ...                 "reduction_perc": 50
    ...             },
    ...             {
    ...                 "applied": "2021-01-01T00:00:00.000Z",
    ...                 "reduction_perc": 75
    ...             },
    ...         ]
    ...     }})
    False

    """

    # Identify all the payment reductions applied within the last 90 days.
    payment_reductions_list = [
        x
        for x in payload["loc_record"]["modification"]
        if datetime.strptime(x["applied"], "%Y-%m-%dT%H:%M:%S.%fZ")
        >= (datetime.today() - timedelta(days=90))
        if x["reduction_perc"] > 0
    ]

    # Fail if 2 or more reductions were identified.
    return len(payment_reductions_list) >= 2


@rule(rule_id="PR-002-U1", name="75% of Principal Paid")
def seventy_five_percent_principal_paid(_, payload):
    """
    Unblock if 75% of the principal balance has been paid following the most recent payment.

    >>> seventy_five_percent_principal_paid(None, {"loc_record": {
    ...         "principal_balance": 2500,
    ...         "draw": [
    ...             {
    ...                 "draw_date": "2021-08-01T00:00:00.000Z",
    ...                 "amount": 3000.00,
    ...                 "principal_post_draw": 12000.00
    ...             },
    ...             {
    ...                 "draw_date": "2019-07-01T00:00:00.000Z",
    ...                 "amount": 2000.00,
    ...                 "principal_post_draw": 15000.00
    ...             }
    ...         ]
    ...     }})
    True
    >>> seventy_five_percent_principal_paid(None, {"loc_record": {
    ...         "principal_balance": 8000,
    ...         "draw": [
    ...             {
    ...                 "draw_date": "2021-08-01T00:00:00.000Z",
    ...                 "amount": 3000.00,
    ...                 "principal_post_draw": 12000.00
    ...             },
    ...             {
    ...                 "draw_date": "2019-07-01T00:00:00.000Z",
    ...                 "amount": 2000.00,
    ...                 "principal_post_draw": 15000.00
    ...             }
    ...         ]
    ...     }})
    False
    """
    # Calculate the required balance threshold (i.e. 25% of the actual balance following the latest draw).
    balance_threshold = 0
    if len(payload["loc_record"]["draw"]) > 0:
        balance_threshold = (
            payload["loc_record"]["draw"][0]["principal_post_draw"] * 0.25
        )

    # Fail if balance required is greater than the account principal balance.
    return payload["loc_record"]["principal_balance"] <= balance_threshold


@rule(rule_id="PR-003-B1", name="Two Consecutive Payment Reductions")
def two_consecutive_payment_reductions(_, payload):
    """
    Block if there are two 2 consecutive payment reductions.

    >>> two_consecutive_payment_reductions(None, {"loc_record": {
    ...         "modification": [
    ...             {
    ...                 "mod_cluster": 1,
    ...                 "reduction_perc": 50,
    ...             },
    ...             {
    ...                 "mod_cluster": 2,
    ...                 "reduction_perc": 75,
    ...             },
    ...             {
    ...                 "applied": "2021-06-01T00:00:00.000Z",
    ...                 "mod_cluster": 3,
    ...                 "reduction_perc": 75,
    ...             }
    ...         ]
    ...     }})
    True
    >>> two_consecutive_payment_reductions(None, {"loc_record": {
    ...         "modification": [
    ...             {
    ...                 "mod_cluster": 1,
    ...                 "reduction_perc": 50,
    ...             },
    ...             {
    ...                 "mod_cluster": 1,
    ...                 "reduction_perc": 75,
    ...             },
    ...             {
    ...                 "mod_cluster": 2,
    ...                 "reduction_perc": 75,
    ...             }
    ...         ]
    ...     }})
    False
    """

    # Create a list of payment modifications grouped by their consecutive clustering
    clusters = {}
    for mod in payload["loc_record"]["modification"]:
        if mod["reduction_perc"] > 0:
            if str(mod["mod_cluster"]) not in clusters:
                clusters[str(mod["mod_cluster"])] = []
            clusters[str(mod["mod_cluster"])].append(mod)

    # Check if any of the clusters contain more than 1 payment modifications
    consecutive_reductions_found = False
    for c in clusters.keys():
        if len(clusters[c]) > 1:
            consecutive_reductions_found = True

    # Fail if any consecutive reductions were found
    return consecutive_reductions_found is not True


@rule(rule_id="PR-003-U2", name="No Reductions Since Latest Draw")
def no_reductions_since_latest_draw(_, payload):
    """
    Unblock if there have been payment reduction has taken place since the last time a draw was made on the account.

    >>> no_reductions_since_latest_draw(None, {"loc_record": {
    ...         "draw": [
    ...             {
    ...                 "draw_date": "2021-08-01T00:00:00.000Z",
    ...                 "amount": 5000.00,
    ...                 "principal_post_draw": 12000.00
    ...             },
    ...             {
    ...                 "draw_date": "2019-07-01T00:00:00.000Z",
    ...                 "amount": 2000.00,
    ...                 "principal_post_draw": 17000.00
    ...             }
    ...         ],
    ...         "modification": [
    ...             {
    ...                 "applied": "2021-07-01T00:00:00.000Z",
    ...                 "suspended": "2021-07-21T00:00:00.000Z",
    ...                 "mod_cluster": 1,
    ...                 "reduction_perc": 50,
    ...                 "instalment_amount": 200.05
    ...             },
    ...             {
    ...                 "applied": "2021-06-01T00:00:00.000Z",
    ...                 "suspended": "2021-06-14T00:00:00.000Z",
    ...                 "mod_cluster": 2,
    ...                 "reduction_perc": 75,
    ...                 "instalment_amount": 125.00
    ...             }
    ...         ]
    ...     }})
    True
    >>> no_reductions_since_latest_draw(None, {"loc_record": {
    ...        "draw": [
    ...            {
    ...                "draw_date": "2021-08-01T00:00:00.000Z",
    ...                "amount": 5000.00,
    ...                "principal_post_draw": 12000.00
    ...            },
    ...            {
    ...                "draw_date": "2019-07-01T00:00:00.000Z",
    ...                "amount": 2000.00,
    ...                "principal_post_draw": 17000.00
    ...            }
    ...        ],
    ...        "modification": [
    ...            {
    ...                "applied": "2021-08-8T00:00:00.000Z",
    ...                "suspended": "2021-08-25T00:00:00.000Z",
    ...                "mod_cluster": 1,
    ...                "reduction_perc": 50,
    ...                "instalment_amount": 200.05
    ...            },
    ...            {
    ...                "applied": "2021-06-01T00:00:00.000Z",
    ...                "suspended": "2021-06-14T00:00:00.000Z",
    ...                "mod_cluster": 2,
    ...                "reduction_perc": 75,
    ...                "instalment_amount": 125.00
    ...            },
    ...        ]
    ...    }})
    False
    """

    # Get the date of the latest draw. If there are no draws then use a default 'early date'.
    latest_draw_date = "1900-01-01T00:00:00Z"
    if len(payload["loc_record"]["draw"]) > 0:
        latest_draw_date = payload["loc_record"]["draw"][0]["draw_date"]

    # Identify any payment reductions that were applied after the latest draw date.
    payment_reductions_list = [
        x
        for x in payload["loc_record"]["modification"]
        if x["applied"] > latest_draw_date
        if x["reduction_perc"] > 0
    ]

    # Fail if any payment reductions were identified.
    return len(payment_reductions_list) == 0


@rule(rule_id="PR-004-B1", name="On Payment Holiday")
def on_payment_holiday(_, payload):
    """
    Block if the account is currently subject to an agreed payment holiday.

    >>> on_payment_holiday(None, {"loc_record": {
    ...         "modification": [
    ...             {
    ...                 "applied": "2021-07-01T00:00:00.000Z",
    ...                 "suspended": "2021-12-01T00:00:00.000Z",
    ...                 "instalment_amount": 0
    ...             }
    ...         ]
    ...     }})
    True
    >>> on_payment_holiday(None, {"loc_record": {
    ...         "modification": [
    ...             {
    ...                 "applied": "2021-07-01T00:00:00.000Z",
    ...                 "suspended": None,
    ...                 "instalment_amount": 0
    ...             }
    ...         ]
    ...     }})
    True
    >>> on_payment_holiday(None, {"loc_record": {
    ...         "modification": [
    ...             {
    ...                 "applied": "2021-07-01T00:00:00.000Z",
    ...                 "suspended": "2021-08-01T00:00:00.000Z",
    ...                 "instalment_amount": 0
    ...             }
    ...         ]
    ...     }})
    False
    """

    # Identify if there are any active payment holiday modifications
    payment_holidays = [
        x
        for x in payload["loc_record"]["modification"]
        if x["instalment_amount"] == 0
        if datetime.strptime(x["applied"], "%Y-%m-%dT%H:%M:%S.%fZ") <= datetime.today()
        if datetime.strptime(
            x["suspended"] or "2070-01-01T00:00:00.000Z", "%Y-%m-%dT%H:%M:%S.%fZ"
        )
        >= datetime.today()
    ]

    # Fail if any active payment holidays are found
    return len(payment_holidays) > 0


@rule(rule_id="PR-004-S1", name="Had Payment Holiday")
def had_payment_holiday(_, payload):
    """
    Supporting rule to indicate whether a an account has previously been on a payment holiday.
    A pass result indicates the account has previously been subject to payment holiday.

    >>> had_payment_holiday(None, {"loc_record": {
    ...         "modification": [
    ...             {
    ...                 "applied": "2021-07-01T00:00:00.000Z",
    ...                 "suspended": "2021-08-01T00:00:00.000Z",
    ...                 "instalment_amount": 0
    ...             }
    ...         ]
    ...     }})
    True
    >>> had_payment_holiday(None, {"loc_record": {
    ...         "modification": [
    ...             {
    ...                 "applied": "2021-07-01T00:00:00.000Z",
    ...                 "suspended": None,
    ...                 "instalment_amount": 0
    ...             }
    ...         ]
    ...     }})
    False
    >>> had_payment_holiday(None, {"loc_record": {
    ...         "modification": [
    ...             {
    ...                 "applied": "2021-07-01T00:00:00.000Z",
    ...                 "suspended": "2021-12-01T00:00:00.000Z",
    ...                 "instalment_amount": 0
    ...             }
    ...         ]
    ...     }})
    False
    """

    # Pass if there are any previous, non-active payment holiday account modifications.
    return (
        len(
            [
                x
                for x in payload["loc_record"]["modification"]
                if x["instalment_amount"] == 0
                if datetime.strptime(x["applied"], "%Y-%m-%dT%H:%M:%S.%fZ")
                < datetime.today()
                if x["suspended"] is not None
                if datetime.strptime(
                    x["suspended"] or "2070-01-01T00:00:00.000Z",
                    "%Y-%m-%dT%H:%M:%S.%fZ",
                )
                < datetime.today()
            ]
        )
        > 0
    )


@rule(
    rule_id="PR-004-U1",
    name="Three Consecutive Payments Since Payment Holiday",
    run_if=had_payment_holiday,
)
def three_consecutive_payments_since_payment_holiday(_, payload):
    """
    Unblock if three consecutive, non-reduced payments have been made since the last payment holiday ended.

    >>> three_consecutive_payments_since_payment_holiday(None, {"loc_record": {"current_cons_full_pmt": 3}})
    True
    >>> three_consecutive_payments_since_payment_holiday(None, {"loc_record": {"current_cons_full_pmt": 2}})
    False
    """

    # Fail if current numebr of consectutive full payments is less then 3.
    return payload["loc_record"]["current_cons_full_pmt"] >= 3


block_on_one_missed_payment = All(
    "MP-001",
    "Block On One Missed Payment",
    days_not_paid,
    two_consecutive_payments_made,
    description="Customer has missed their latest payment.",
)

block_on_two_missed_payments = All(
    "MP-002",
    "Block On Two Missed Payments",
    two_missed_payments,
    three_consecutive_payments_made,
    description="Customer has missed two payments in the last three months.",
)

block_on_three_missed_payments = All(
    "MP-003",
    "Block On Three Missed Payments",
    three_missed_payments,
    four_consecutive_payments_made,
    description="Customer has missed three payments in the last three months.",
)

block_on_more_than_three_missed_payments = All(
    "MP-004",
    "Block On More Than Three Missed Payments",
    more_than_three_missed_payments,
    six_consecutive_payments_made,
    description="Customer has missed more than three payments in the last six months.",
)

missed_payments = All(
    "MP",
    "Missed Payments",
    block_on_one_missed_payment,
    block_on_two_missed_payments,
    block_on_three_missed_payments,
    block_on_more_than_three_missed_payments,
    description="Accounts blocks caused by missing or late payments.",
)


block_on_two_payment_reductions_in_180_days = All(
    "PR-001",
    "Block on Two Payment Reductions in 180 Days",
    two_payment_reductions_in_180_days,
    fifty_percent_principal_paid,
    no_reductions_since_latest_draw,
    description="There have been two payment reductions in the last 180 days.",
)

block_on_two_payment_reductions_in_90_days = All(
    "PR-002",
    "Block on Two Payment Reductions in 90 Days",
    two_payment_reductions_in_90_days,
    seventy_five_percent_principal_paid,
    no_reductions_since_latest_draw,
    description="There have been two payment reductions in the last 90 days.",
)

block_on_two_consecutive_payment_reductions = All(
    "PR-003",
    "Block on Two Consecutive Payment Reductions",
    two_consecutive_payment_reductions,
    seventy_five_percent_principal_paid,
    no_reductions_since_latest_draw,
    description="There have been two payment reductions in the last 90 days.",
)

block_on_payment_holiday = All(
    "PR-004",
    "Block on Payment Holiday",
    on_payment_holiday,
    three_consecutive_payments_since_payment_holiday,
    description="The account is subject to an agreed payment holiday.",
)

payment_reductions = All(
    "PR",
    "Payment Reductions",
    block_on_two_payment_reductions_in_180_days,
    block_on_two_payment_reductions_in_90_days,
    block_on_two_consecutive_payment_reductions,
    block_on_payment_holiday,
    description="Accounts blocks caused by multiple payment reductions.",
)


account_status = All(
    "account_status",
    "Account Status",
    missed_payments,
    payment_reductions,
    description="Overall status for the account, where failure indicates that the account should be blocked.",
)

nest_10 = All(
    "nest_10",
    "Nest 10 this name is super super super super super super super super super super long",
    days_not_paid,
    description="Nest stress test",
)

nest_9 = All(
    "nest_9",
    "Nest 9",
    nest_10,
    description="Nest stress test",
)

nest_8 = All(
    "nest_8",
    "Nest 8",
    nest_9,
    description="Nest stress test",
)

nest_7 = All(
    "nest_7",
    "Nest 7 this name is very descriptive and probably too long to be useful",
    nest_8,
    description="Nest stress test",
)

nest_6 = All(
    "nest_6",
    "Nest 6 short name again",
    nest_7,
    description="Nest stress test",
)

nest_5 = All(
    "nest_5",
    "Nest 5 This name is very long, even longer than the last",
    nest_6,
    description="Nest stress test",
)

nest_4 = All(
    "nest_4",
    "Nest 4 an even longer name here to fill space",
    nest_5,
    description="Nest stress test",
)

nest_3 = All(
    "nest_3",
    "Nest 3 middle length name",
    nest_4,
    description="Nest stress test",
)

nest_2 = All(
    "nest_2",
    "Nest 2 short name",
    nest_3,
    description="Nest stress test",
)

nest_1 = All(
    "nest_1",
    "Nest 1",
    nest_2,
    description="Nest stress test",
)
