from typing import TYPE_CHECKING, Any, AnyStr, Dict, Optional, TypedDict


class ErrorMessage(TypedDict):
    error_name: str
    error_message: str
