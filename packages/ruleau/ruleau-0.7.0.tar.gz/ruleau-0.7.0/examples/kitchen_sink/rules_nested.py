from ruleau import All, Process, execute, rule
from ruleau.adapter import ApiAdapter


# create a rule
@rule(rule_id="rul_01", name="over_18")
def over_18(context, payload):
    """
    Check applicant over 18
    >>> age(None, {"age": 18})
    True
    >>> age(None, {"age": 17})
    False
    """
    return "age" in payload and payload["age"] >= 18


@rule(rule_id="rul_02", name="not_short", depends_on=[over_18])
def not_short(context, payload):
    """
    Check applicant isn't short
    """
    return (
        context.get_result(over_18).result
        and "height" in payload
        and payload["height"] == "tall"
    )


collection = All(
    "rul_03",
    "Age Checker",
    All("rul_04", "sub level", over_18, All("rul_05", "sub sub level", not_short)),
)

# create a payload (the answers to the rule's questions)
payload = {"age": 18, "height": "tall", "case_id": "testing-xx"}
api_adapter = ApiAdapter(base_url="http://localhost:8000/")
process = Process.create_process_from_rule(collection)
api_adapter.sync_process(api_adapter)
# send the results
result = execute(
    collection,
    payload,
    process,
    # api_adapter=api_adapter,
    case_id_jsonpath="$.case_id",
)
print(f"result: {result.result}")
