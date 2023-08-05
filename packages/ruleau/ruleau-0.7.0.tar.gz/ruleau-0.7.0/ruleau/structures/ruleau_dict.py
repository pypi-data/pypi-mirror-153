import inspect
import os
from collections.abc import MutableMapping
from copy import deepcopy
from json import dumps

from flatdict import FlatDict

from ruleau.exceptions import MethodNotAllowedException


class RuleauDict(MutableMapping):
    """
    RuleauDict is an immutable, dictionary lookalike mapping which allows the
    library to track how many times a key is used inside a payload.

    It provides a public property `.accessed` which returns all the accessed
    keys with their count and types

    >>> RuleauDict({"value": 1})
    <RuleauDict {'a': 1}>

    """

    _key: str = "__ruleau_key__"
    _value: str = "__ruleau_value__"
    _type: str = "__ruleau_type__"
    _accessed_count: str = "__ruleau_accessed_count__"

    def __init__(self, data):
        """
        Initialize RuleauDict with the dictionary passed by the user
        :param data:
        """
        super().__init__()
        self._data = {}
        self._original_data = deepcopy(data)
        self._encode(deepcopy(data))
        # Set exception debug information
        info = RuleauDict._get_relevant_call_stack_info()
        self.line_number = info["lineno"]
        self.file_name = info["filename"]

    def __getitem__(self, key):
        """
        Accessor function to get the dictionary values and increment accessed count
        :param key:
        :return:
        """
        # If the value is accessed, increment the counter
        self._data[key][self._accessed_count] += 1
        return self._data[key][self._value]

    def __repr__(self):
        return f"<RuleauDict {dumps(self._original_data)}>"

    def __delitem__(self, key):
        raise MethodNotAllowedException(rule_dict=self, method="__delitem__")

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

    def __setitem__(self, key, value):
        raise MethodNotAllowedException(rule_dict=self, method="__setitem__")

    def __eq__(self, other):
        return self._original_data == other

    def __ne__(self, other):
        return self._original_data != other

    @staticmethod
    def _get_relevant_call_stack_info():
        found_rule_dict = False
        result = {"lineno": None, "filename": None}
        files_to_skip = {"process.py", "execute.py"}
        current_frame = inspect.currentframe()
        while current_frame:
            filename = current_frame.f_code.co_filename
            if filename.endswith("rule.py"):
                found_rule_dict = True
            elif found_rule_dict and os.path.basename(filename) not in files_to_skip:
                result["filename"] = filename
                result["lineno"] = current_frame.f_lineno
                break
            current_frame = current_frame.f_back
        return result

    def items(self):
        return self._original_data.items()

    def _encode(self, data) -> None:
        """
        Method to encode the dictionary into RuleauDict structure
        :param data:
        """
        for key, value in data.items():
            self._data[key] = {
                self._key: key,
                self._value: RuleauDict(value) if isinstance(value, dict) else value,
                self._type: type(value).__name__,
                self._accessed_count: 0,
            }

    def _decode(self):
        """
        Method to decode the RuleauDict into a nested dictionary with all metadata
        :return: Decoded dictionary with all internal values
        """
        data = {}
        for key, value in self._data.items():
            obj = deepcopy(value)
            obj.update({self._value: self._decode_value(obj[self._value])})
            data[key] = obj
        return data

    def _decode_value(self, value):
        """
        Helper function to decode the final value of the dictionary
        :param value:
        :return: Normalized decoded value
        """
        return value._decode() if isinstance(value, RuleauDict) else value

    @property
    def accessed(self):
        """
        Processes the result of the how many times a key was accessed.
        :return: Dictionary of items that were accessed with it's count
        """
        decoded_flattened = FlatDict(self._decode(), ".")
        original_flattened = FlatDict(self._original_data, ".")
        accessed_keys = [
            x
            for x in decoded_flattened
            if self._accessed_count in x and decoded_flattened[x] > 0
        ]
        accessed_values = []
        for accessed_key in accessed_keys:
            original_value_key = accessed_key.replace(
                f".{self._accessed_count}", ""
            ).replace(f".{self._value}", "")
            type_key = accessed_key.replace(self._accessed_count, self._type)
            accessed_values.append(
                {
                    "key": original_value_key,
                    "accessed_count": decoded_flattened[accessed_key],
                    "type": decoded_flattened[type_key],
                    "value": original_flattened[original_value_key].as_dict()
                    if isinstance(original_flattened[original_value_key], FlatDict)
                    else original_flattened[original_value_key],
                }
            )
        return accessed_values
