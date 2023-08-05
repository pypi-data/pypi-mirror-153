from ruleau import All

from .shared_rules.rules import is_registered

composed_from_package = All("ID", "name", is_registered)
