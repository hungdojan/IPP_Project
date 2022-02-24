"""File contains core structure of interpreter IPPcode22

Author: Hung Do
File:   coredata.py
Module: proj2_module
"""
import sys
from .error import ErrorCode
from .frame import Frame, Variable

UNICODE_MAX_VAL = 1,114,111

class CoreData:
    input_file = None
    source_file = None
    REG_TYPE = {
            'var': r'(GF|LF|TF)@[a-zA-Z_$&%*!?-][a-zA-Z0-9_$&%*!?-]*',
            'string': '([^\s#\\\\]|\\\\\d{3})+',
            'float': r'[+-]?(\d*(\.\d))?',
            'float_hex': r'[+-]?(0x)?[01]\.?[0-9a-f]*(p[+-]?[0-9a-f]+)?',
            'int': r'[+-]?\d+',
            'label': '[a-zA-Z_$&%*!?-][a-zA-Z0-9_$&%*!?-]*',
            'type': '(int|bool|string|float)'
            }

    global_frame: Frame = Frame()
    temp_frame: Frame   = None
    local_frame: Frame  = None
    labels = {}
    undef_labels = []
    ins_performed = 0

    stack_func = []
    stack_frames = []
    stack_vals = []

    @classmethod
    def add_variable(cls, var_name: str):
        """Adds variable to frame

        Checks variable name's prefix and decides, to which frame new variable
        has to be inserted.

        Parameters:
        var_name (str): Variable name

        """
        simplified_name = Variable.simplify_var_name(var_name)

        # get frame from variable prefix
        if var_name.startswith('GF@'):
            cls.global_frame.add_variable(simplified_name)
        elif var_name.startswith('LF@'):
            if cls.local_frame is None:
                sys.exit(ErrorCode.RUNTIME_NONEXIST_FRAME)
            cls.local_frame.add_variable(simplified_name)
        else:
            if cls.temp_frame is None or not cls.temp_frame.is_active:
                sys.exit(ErrorCode.RUNTIME_NONEXIST_FRAME)
            cls.temp_frame.add_variable(simplified_name)

    @classmethod
    def get_variable(cls, var_name: str):
        """Returns stored variable from frame

        Check variable name's prefix and decides, which frame to look in for.
        Terminate program with ErrorCode.RUNTIME_NONEXIST_FRAME if frame is
        not 

        Parameters:
        var_name (str): Variable name

        """
        simplified_name = Variable.simplify_var_name(var_name)

        # get frame from variable prefix
        if var_name.startswith('GF@'):
            return cls.global_frame.get_var(simplified_name)
        elif var_name.startswith('LF@'):
            if cls.local_frame is None:
                sys.exit(ErrorCode.RUNTIME_NONEXIST_FRAME)
            return cls.local_frame.get_var(simplified_name)
        else:
            if cls.temp_frame is None or not cls.temp_frame.is_active:
                sys.exit(ErrorCode.RUNTIME_NONEXIST_FRAME)
            return cls.temp_frame.get_var(simplified_name)

    @classmethod
    def get_symbol(cls, argument):
        """Return a symbol (variable or constant) from argument

        Parameters:
        argument (Argument): Instance of argument

        Returns:
        TODO:
        """
        if argument.type == 'var':
            var: Variable = cls.get_variable(argument.value)
            return var
        else:
            return argument

    @classmethod
    def get_line(cls):
        """Return read data from stdin or input file

        Returns:
        str: Read data
        
        """
        if cls.input_file is None:
            return input()
        return cls.input_file.readline().rstrip()


    @classmethod
    def set_jumps(cls, lof_ins):
        """Set jump destinations to labels"""
        for i in range(len(lof_ins)):
            stat = lof_ins[i]
            if stat.ins == 'LABEL':
                cls.labels[stat.args[0].value] = i+1
