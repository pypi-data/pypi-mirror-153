import argparse
import importlib
import json
import os
import sys
from argparse import Namespace
from os import mkdir, path
from typing import AnyStr, List, Optional

from jinja2 import Template
from jinja2.filters import FILTERS, environmentfilter

from ruleau.documentation_enrichment_functions import enrich_rules
from ruleau.exceptions import (
    CouldNotImportRulesToDocument,
    IncorrectTypeProvidedForImport,
)
from ruleau.rule import Rule


@environmentfilter
def json_print(_, value):
    """Pretty print json filter for jinja2"""
    value = value if isinstance(value, dict) or value is None else json.loads(value)
    return json.dumps(
        value,
        sort_keys=True,
        indent=4,
        separators=(",", ": "),
    )


@environmentfilter
def filter_runif_dependencies(_, dependencies):
    return [dep for dep in dependencies if dep["run_if"]]


@environmentfilter
def filter_non_runif_dependencies(_, dependencies):
    return [dep for dep in dependencies if not dep["run_if"]]


#  Add the json_print filter to jinja2 filters
FILTERS["json_print"] = json_print
FILTERS["filter_runif"] = filter_runif_dependencies
FILTERS["filter_non_runif"] = filter_non_runif_dependencies


def order_rules(rules: List["Rule"]) -> List["Rule"]:
    """Order rules so top level rules appear first"""
    is_root = {rule: True for rule in rules}

    # If any rule is dependent on a rule then it is not the root
    for rule in rules:
        for dependent in rules:
            if dependent != rule and dependent in rule.dependencies:
                is_root[dependent] = False

    roots = [rule for rule, is_root_rule in is_root.items() if is_root_rule]
    others = [rule for rule, is_root_rule in is_root.items() if not is_root_rule]
    return roots + others


def generate_documentation(rules: List["Rule"]) -> AnyStr:
    """Returns a HTML string, documenting the passed in rule and its dependents

    :param rules: List of rules to generate document of
    """
    with open(
        path.join(path.dirname(path.realpath(__file__)), "html", "documentation.html")
    ) as f:
        doc_template = Template(f.read())

    logo_path = path.join(path.dirname(path.realpath(__file__)))

    logo_path = path.join(logo_path, "html", "images", "RuleauLogo_Black.png")

    rules = order_rules(rules)
    enriched_rules_dict = enrich_rules(rules)

    #  for rule  in enriched_rules_dict:
    #  colors = {
    #  "light": "75FF96",
    #  "primary": "12C170",
    #  "dark": "17764A",
    #  }

    return doc_template.render(rules=enriched_rules_dict, logo_path=logo_path)


def get_dependencies(rule: "Rule", rule_list: Optional[List] = None):
    """Recursively adds the rule dependencies to a list
    :param rule: The Rule to add dependencies for.
    :param: rule_list: An optional list of dependencies that
     are already known to exist.
    :return: rule_list: A list of Rule dependencies.
    """
    if rule_list is None:
        rule_list = []
    if rule not in rule_list:
        rule_list.append(rule)
    for dependency in rule.dependencies:
        get_dependencies(dependency, rule_list)
    return rule_list


def render_doc_for_module(module_file, top_level_rule) -> AnyStr:
    """Render the documentation from a rule module
    :param module_file:
    :param top_level_rule: The top level rule that is dependent on all other rules.
    :return:
    """
    # Need the path of the rules
    rule_path = path.split(path.abspath(module_file))[0]

    # Module name is different to the module path
    module_name = path.splitext(module_file)[0]
    # Formatting for the module registering
    # Formatting for a Windows Path
    module_name = module_name.replace("\\", ".")
    # Formatting for a Nix path
    module_name = module_name.replace("/", ".")
    # Remove any trailing "." characters (e.g: from when './module.py' is passed in)
    module_name = module_name.lstrip(".")

    sys.path.append(rule_path)

    spec = importlib.util.spec_from_file_location(module_name, module_file)
    config = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = config

    # Append the current working directory for any package imports
    # in the referenced script
    cwd = os.getcwd()
    if cwd not in sys.path:
        sys.path.append(cwd)

    try:
        spec.loader.exec_module(config)
    except ModuleNotFoundError as ex:
        raise CouldNotImportRulesToDocument(module_file, top_level_rule, ex)

    rule_instance = getattr(config, top_level_rule)

    if not isinstance(rule_instance, Rule):
        raise IncorrectTypeProvidedForImport(module_file, top_level_rule)

    # Pick rules to document
    rules = get_dependencies(rule_instance)
    return generate_documentation(rules)


def generate_and_save_to_file(input_files, output_dir):
    """Generate the documentation and save to a file in provided output dir
    :param input_files: Rule modules and top level function names provided by
     user via CLI
    :param output_dir: Output directory of generated HTML file
    """

    generated_docs = []

    if len(input_files) == 0:
        raise Exception("No file(s) supplied to generate documentation for.")

    if not path.exists(output_dir):
        mkdir(output_dir)

    for target_file in input_files:
        if target_file.split("::") == [target_file]:
            raise ValueError(
                "Please provide a name of top level function. "
                f"Required format is {target_file}::function_name."
            )
        top_level_rule = target_file.split("::")[1]
        target_file = target_file.split("::")[0]
        if not path.exists(target_file):
            raise ValueError(f"{target_file} does not exist")

        documentation = render_doc_for_module(target_file, top_level_rule)

        output_filename = path.join(
            output_dir, "{}.html".format(path.basename(target_file).split(".")[0])
        )

        with open(output_filename, "w") as f:
            f.write(documentation)
        generated_docs.append(output_filename)

    print(
        f"{len(generated_docs)} doc{'s' if len(generated_docs) > 1 else ''} generated."
    )
    print("\n".join(generated_docs))


def get_arguments(args) -> Namespace:
    """Parses arguments for the ruleau-docs command
    :param args:
    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output-dir",
        dest="output_dir",
        default="./",
        help="Directory for generated documents",
    )
    parser.add_argument("files", nargs="*")
    return parser.parse_args(args)


def main() -> int:  # pragma: no cover
    """Console script for deft document generation.
    USAGE:
    ```bash
    $ ruleau-docs [--output-dir=<argument>] filename ...
    ```
    """
    args = get_arguments(sys.argv[1:])
    generate_and_save_to_file(args.files, args.output_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
