from logging import getLogger
from typing import AnyStr, List, Optional

import requests

from ruleau.constants import OverrideLevel
from ruleau.rule import Rule

logger = getLogger(__name__)
logger.propagate = True


def api_request(func):
    def _api_request(*args, **kwargs) -> Optional[dict]:
        try:
            if args:
                args[0]._check_access_token_is_active()
                args[0]._create_requests_session()
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Exception occurred: {e}")
            raise e

    return _api_request


def rule(
    rule_id: AnyStr,
    name: AnyStr,
    depends_on: Optional[List[Rule]] = None,
    override_level: OverrideLevel = OverrideLevel.ENABLED,
    run_if: Optional[Rule] = None,
    run_if_not: Optional[Rule] = None,
):
    """Decorator to encapsulate a function into a rule"""
    depends_on = depends_on or []

    def _rule(func) -> Rule:
        return Rule(func, rule_id, name, depends_on, override_level, run_if, run_if_not)

    return _rule
