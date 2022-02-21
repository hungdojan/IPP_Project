import sys
import re
from .error import ErrorCode

class Variable:

    def __init__(self):
        self._value = None
        self._type = 'UNDEF'

    @property
    def type(self):
        return self._type

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
        if value is None:
            self._type = 'nil'
        elif isinstance(value, int):
            self._type = 'int'
        elif isinstance(value, str):
            self._type = 'string'
        elif isinstance(value, bool):
            self._type = 'bool'
        elif isinstance(value, float):
            self._type = 'float'
        else:
            sys.exit(ErrorCode.UNDEFINED_ERROR)

    @staticmethod
    def simplify_var_name(var_name: str):
        """ Removes prefixes GF@, LF@, TF@ """
        return re.sub("^(GF|LF|TF)@", "", var_name)

    def __str__(self):
        return f"[{self._type}: {self._value}]"

    def __repr__(self):
        return str(self)

class Frame:

    def __init__(self):
        self.is_active = True
        self.vars = {}

    def add_variable(self, var_name: str):
        # check if variable exists
        if self.vars.get(var_name) is not None:
            sys.exit(ErrorCode.SEMANTIC_ERROR)
        self.vars[var_name] = Variable()

    def get_var(self, var_name: str):
        var = self.vars.get(var_name)
        # check if variable exists
        if var is None:
            sys.exit(ErrorCode.RUNTIME_UNDEF_VAR)
        return var
