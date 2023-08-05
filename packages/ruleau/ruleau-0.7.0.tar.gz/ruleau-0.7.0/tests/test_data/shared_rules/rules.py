from ruleau import rule


@rule(rule_id="rul_01", name="is_registered")
def is_registered(context, payload):
    """
    Check person is registered
    >>> is_registered(None, {"registered": True})
    True
    >>> is_registered(None, {"registered": False})
    False
    """
    return "registered" in payload and payload["registered"]
