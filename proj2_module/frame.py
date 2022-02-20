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

    def _format_str(self):
        # TODO: format string \032 -> ' '
        pass

    @staticmethod
    def simplify_var_name(var_name: str):
        """ Removes prefixes GF@, LF@, TF@ """
        return re.sub("^(GF|LF|TF)@", "", var_name)

    def __str__(self):
        return ""

    def __repr__(self):
        return str(self)

class Frame:

    def __init__(self):
        self.is_active = True
        self._var_names = []
        self.vars = {}

    def add_variable(self, var_name: str):
        if var_name in self._var_names:
            sys.exit(ErrorCode.SEMANTIC_ERROR)
        self._var_names.append(var_name)
        self.vars[var_name] = Variable()

    def get_var(self, var_name: str):
        if var_name not in self._var_names:
            sys.exit(ErrorCode.RUNTIME_UNDEF_VAR)
        return self.vars[var_name]
