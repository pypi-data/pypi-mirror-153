from doesnt_exist.test_data.shared_rules.rules import is_registered

from ruleau import All

composed_from_package = All("ID", "name", is_registered)
