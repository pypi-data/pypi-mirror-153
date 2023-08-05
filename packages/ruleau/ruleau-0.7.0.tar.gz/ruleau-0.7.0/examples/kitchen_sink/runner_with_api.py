from examples.kitchen_sink.rules import will_lend
from ruleau import ApiAdapter, Process, execute

if __name__ == "__main__":
    # Add API adapter to runner
    api_adapter = ApiAdapter(base_url="http://127.0.0.1:8000").with_organisational_data(
        [{"key": "Data Name", "value": None}]
    )
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
        case_id="abc",
    )
