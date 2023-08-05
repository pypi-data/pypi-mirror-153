from ruleau import All
from tests.test_data.shared_rules.rules import is_registered


def composed_from_package():
    return All("ID", "name", is_registered)
