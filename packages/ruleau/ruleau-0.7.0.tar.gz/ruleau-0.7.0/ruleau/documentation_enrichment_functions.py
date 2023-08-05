import collections
from typing import Dict, List


# There is an issue where test coverage can't unpack next iteration
def calculate_rules_depends_on(rules: List) -> List:  # pragma: no cover
    """
    Calculate rules depends_on using dependencies of parent rules
    """
    for rule in rules:
        for dependency in rule["dependencies"]:
            dependency_list_position = next(
                (
                    i
                    for i, rule_dict in enumerate(rules)
                    if rule_dict["id"] == dependency["id"]
                )
            )
            rules[dependency_list_position]["depends_on"].append(rule["id"])
    return rules


def calculate_rules_breadcrumbs(rules_dict: Dict[str, Dict]) -> Dict[str, Dict]:
    """
    Calculate rule breadcrumb trail to top level rule
    """
    for rule_id in rules_dict:
        depends_on_dict = calculate_rule_depends_on_hierarchies(rule_id, rules_dict)
        depends_on_breadcrumbs = flatten_rule_depends_on_hierarchies(depends_on_dict)
        rules_dict[rule_id]["depends_on_breadcrumbs"] = depends_on_breadcrumbs

    return rules_dict


def calculate_rule_depends_on_hierarchies(
    rule_id: str, rules_dict: Dict[str, Dict]
) -> Dict[str, Dict]:
    """
    Extract hierarchy of depends_on for a given rule
    """
    rule = rules_dict[rule_id]
    depends_on_dict = {}
    for depends_on_id in rule["depends_on"]:
        depends_on_dict[depends_on_id] = calculate_rule_depends_on_hierarchies(
            depends_on_id, rules_dict
        )

    return depends_on_dict


def flatten_rule_depends_on_hierarchies(depends_on_dict: Dict) -> List:
    """
    Flatten hierarchy of depends_on for a given rule
    Creates multiple hierarchies if one-to-many/many-to-one relationships between rules
    """
    depends_on_lists = convert_rule_depends_on_dict_to_lists(depends_on_dict)
    flattened_lists = []

    if depends_on_lists:
        for depends_on_list in depends_on_lists:
            flattened_list = list(flatten_rule_hierarchy(depends_on_list))
            reversed_list = flattened_list[::-1]
            flattened_lists.append(reversed_list)

    return flattened_lists


def convert_rule_depends_on_dict_to_lists(depends_on_dict: Dict) -> List:
    """
    Convert depends_on dictionaries to nested lists structure
    """
    list_collector = []

    for key in depends_on_dict.keys():
        nested_items = convert_rule_depends_on_dict_to_lists(depends_on_dict[key])
        if nested_items:
            for nested_item in nested_items:
                unpacking_list = [key, nested_item]
                list_collector.append(unpacking_list)
        else:
            unpacking_list = [key]
            list_collector.append(unpacking_list)

    if list_collector:
        return list_collector


def flatten_rule_hierarchy(hierarchy: List[List]) -> List:
    """
    Flattens nested lists
    """
    for nested_rule in hierarchy:
        if isinstance(nested_rule, collections.abc.Iterable) and not isinstance(
            nested_rule, (str, bytes)
        ):
            yield from flatten_rule_hierarchy(nested_rule)
        else:
            yield nested_rule


def enrich_rules_doctests_metadata(rules_dict: Dict[str, Dict]) -> Dict[str, Dict]:
    """
    Order and index rules doctests (order: True rules -> False rules)
    """
    for rule_id in rules_dict:
        rules_dict[rule_id]["doctests"].sort(key=lambda x: x["result"], reverse=True)
        for doctest_index, doctest in enumerate(rules_dict[rule_id]["doctests"]):
            rules_dict[rule_id]["doctests"][doctest_index]["doctest_no"] = (
                doctest_index + 1
            )
    return rules_dict


def calculate_rules_doctest_stats(rules_dict: Dict[str, Dict]) -> Dict[str, Dict]:
    """
    Calculate aggregated passing/failing results of rules doctests
    """

    for rule_id in rules_dict:
        rule = rules_dict[rule_id]
        if rule["doctests"]:
            passing_doctests = len(
                [
                    doctest
                    for doctest in rule["doctests"]
                    if doctest["result"] == "True\n"
                ]
            )
            failing_doctests = len(
                [
                    doctest
                    for doctest in rule["doctests"]
                    if doctest["result"] == "False\n"
                ]
            )

            if not passing_doctests:
                passing_doctests = "None"
            if not failing_doctests:
                failing_doctests = "None"

            doctest_stats = [
                {
                    "title": "Pass",
                    "doctest_result": "True\n",
                    "total": passing_doctests,
                },
                {
                    "title": "Fail",
                    "doctest_result": "False\n",
                    "total": failing_doctests,
                },
            ]
            rules_dict[rule_id]["doctest_stats"] = doctest_stats

    return rules_dict


def enrich_rules(rules: List) -> Dict[str, Dict]:
    """
    Enriches a list of Rule objects with dependency information from
    rule children and parents
    """
    parsed_rules = [rule.parse() for rule in rules]
    enriched_rules = calculate_rules_depends_on(parsed_rules)
    enriched_rules_dict = {rule["id"]: rule for rule in enriched_rules}
    enriched_rules_dict = calculate_rules_breadcrumbs(enriched_rules_dict)
    enriched_rules_dict = enrich_rules_doctests_metadata(enriched_rules_dict)
    enriched_rules_dict = calculate_rules_doctest_stats(enriched_rules_dict)
    return enriched_rules_dict
