import sys
from .error import ErrorCode
from .frame import Frame, Variable

UNICODE_MAX_VAL = 1,114,111

class CoreData:
    input_file = None
    source_file = None

    global_frame: Frame = Frame()
    temp_frame: Frame   = None
    local_frame: Frame  = None
    labels = {}
    ins_performed = 0

    stack_func = []
    stack_frames = []
    stack_vals = []

    @classmethod
    def add_variable(cls, var_name: str):
        """ Adds variable to frame """
        simplified_name = Variable.simplify_var_name(var_name)

        # get frame from variable prefix
        if var_name.startswith('GF@'):
            cls.global_frame.add_variable(simplified_name)
        elif var_name.startswith('LF@'):
            if cls.local_frame is None:
                sys.exit(ErrorCode.RUNTIME_NONEXIST_FRAME)
            cls.local_frame.add_variable(simplified_name)
        else:
            if cls.temp_frame is None:
                sys.exit(ErrorCode.RUNTIME_NONEXIST_FRAME)
            cls.temp_frame.add_variable(simplified_name)

    @classmethod
    def get_variable(cls, var_name: str):
        """ Returns stored variable from frame """
        simplified_name = Variable.simplify_var_name(var_name)

        # get frame from variable prefix
        if var_name.startswith('GF@'):
            return cls.global_frame.get_var(simplified_name)
        elif var_name.startswith('LF@'):
            if cls.local_frame is None:
                sys.exit(ErrorCode.RUNTIME_NONEXIST_FRAME)
            return cls.local_frame.get_var(simplified_name)
        else:
            if cls.temp_frame is None:
                sys.exit(ErrorCode.RUNTIME_NONEXIST_FRAME)
            return cls.temp_frame.get_var(simplified_name)

    @classmethod
    def get_symbol(cls, argument):
        if argument.type == 'var':
            var: Variable = cls.get_variable(argument.value)
            return var
        else:
            return argument

    @classmethod
    def get_line(cls):
        if cls.input_file is None:
            return input()
        return cls.input_file.readline()
