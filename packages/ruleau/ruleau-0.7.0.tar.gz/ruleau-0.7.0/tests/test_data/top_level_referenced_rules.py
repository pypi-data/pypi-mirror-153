from ruleau import All
from tests.test_data.shared_rules.rules import is_registered

composed_from_package = All("ID", "name", is_registered)
