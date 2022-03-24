"""Frame and Variable classes

Author: Hung Do
File:   statement.py
Module: proj2_module
"""
import sys
import re
from .error import ErrorCode
from .statement import Argument

class Variable(Argument):

    def __init__(self):
        super().__init__()


    @Argument.value.setter
    def value(self, value):
        """Set new value and data type acording to that"""
        self._value = value
        if value is None:
            self._type = 'nil'
        elif isinstance(value, bool):
            self._type = 'bool'
        elif isinstance(value, int):
            self._type = 'int'
        elif isinstance(value, str):
            self._type = 'string'
        elif isinstance(value, float):
            self._type = 'float'
        else:
            sys.exit(ErrorCode.UNDEFINED_ERROR)


    @staticmethod
    def simplify_var_name(var_name: str):
        """Removes prefixes GF@, LF@, TF@ from variable's name

        Parameters:
        var_name (str): Variable's name

        Returns:
        str: Variable's name without prefix

        """
        return re.sub("^(GF|LF|TF)@", "", var_name)


class Frame:

    def __init__(self):
        self.is_active = True
        self._vars = {}


    @property
    def vars(self):
        return self._vars


    def add_variable(self, var_name: str):
        """Adds new variable to the frame

        Parameters:
        var_name (str): Variable's name

        Returns:
        Variable: Instance of Variable when new variable was successfully added
            None otherwise
        """
        # check if variable exists
        if self._vars.get(var_name) is not None:
            return None
        new_var = Variable()
        self._vars[var_name] = new_var
        return new_var


    def get_var(self, var_name: str):
        """Returns variable instance in the frame.

        Parameters:
        var_name (str): Variable's name

        Returns:
        bool: Variable instance if exists; None if no instance was found.

        """
        return self._vars.get(var_name)
