from typing import Callable, Optional, Union

from ruleau.structures import ExecutionResult, RuleauDict

Function = Callable[
    [Optional[ExecutionResult], Optional[RuleauDict]], Union[None, bool]
]
