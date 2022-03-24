"""Statement and Argument classes

Author: Hung Do
File:   statement.py
Module: proj2_module
"""
import re

class Argument:

    def __init__(self, arg: tuple=None):
        self._type = 'UNDEF'
        self._value = None
        if arg is not None:
            self._symbol_init(arg)


    @property
    def type(self):
        return self._type


    @property
    def value(self):
        return self._value


    def _symbol_init(self, arg: tuple):
        """Initialized argument from tuple (type, value)

        Parameters:
        arg (str, Object): Tuple consisted of its data type and value

        """
        self._type = arg[0]
        if self._type == 'string':
            self._format_string(arg[1])
        elif self._type in ('var', 'label', 'type'):
            self._value = arg[1]
        elif self._type == 'bool':
            self._value = arg[1] == 'true'
        elif self._type == 'int':
            self._value = int(arg[1])
        elif self._type == 'float':
            self._value = float.fromhex(arg[1])
        else:   # nil type
            self._value = None


    def _format_string(self, str_val: str):
        """Format string into printable value"""

        def ascii_to_str(match_obj):
            """Convert \XXX format into ascii_char_value"""
            ascii_value = int(match_obj.group(0)[1:])
            return chr(ascii_value)

        if str_val is None:
            self._value = ''
        else:
            self._value = re.sub(r'\\\d{3}', ascii_to_str, str_val)


    def __str__(self):
        return f"[{self._type}: {self._value}]"


    def __repr__(self):
        return str(self)


class Statement:

    def __init__(self, ins, order: int, args: list):
        self.ins   = ins
        self.order = order
        self.args  = [Argument(arg) for arg in args]


    def __str__(self):
        output_msg = f"{self.order}: {self.ins}"
        for arg in self.args:
            output_msg += f" {arg}"
        return output_msg


    def __repr__(self):
        return str(self)
