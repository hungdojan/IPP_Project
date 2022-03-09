"""File contains core structure of interpreter IPPcode22

Author: Hung Do
File:   coredata.py
Module: proj2_module
"""
import sys
from .error import ErrorCode
from .frame import Frame, Variable
from .statement import Statement, Argument

class CoreData:
    input_file: list = None
    _line_index = 0
    source_file = None
    REG_TYPE = {
            'var': r'(GF|LF|TF)@[a-zA-Z_$&%*!?-][a-zA-Z0-9_$&%*!?-]*',
            'string': r'([^\s#\\]|\\\d{3})*',
            'float': r'[+-]?\d*(\.\d+)?',
            'float_hex': r'[+-]?(0x)?[01]\.?[0-9a-f]*(p[+-]?[0-9a-f]+)?',
            'int': r'[+-]?\d+',
            'label': '[a-zA-Z_$&%*!?-][a-zA-Z0-9_$&%*!?-]*',
            'type': '(int|bool|string|float)'
            }

    global_frame: Frame = Frame()
    temp_frame: Frame   = None
    local_frame: Frame  = None
    labels = {}
    undef_labels = set()
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
            new_var = cls.global_frame.add_variable(simplified_name)
        elif var_name.startswith('LF@'):
            if cls.local_frame is None:
                ErrorCode.exit_error(
                        f"Error while calling variable {var_name}\n"
                        "Local frame does not exists.",
                        ErrorCode.RUNTIME_NONEXIST_FRAME)
            new_var = cls.local_frame.add_variable(simplified_name)
        else:
            if cls.temp_frame is None or not cls.temp_frame.is_active:
                ErrorCode.exit_error(
                        f"Error while calling variable {var_name}\n"
                        "Temporary frame does not exists.",
                        ErrorCode.RUNTIME_NONEXIST_FRAME)
            new_var = cls.temp_frame.add_variable(simplified_name)

        if new_var is None:
            ErrorCode.exit_error(
                    "Error while creating new variable:\n"
                    f"Variable {var_name} already exists",
                    ErrorCode.SEMANTIC_ERROR)

    @classmethod
    def get_variable(cls, var_name: str) -> Variable:
        """Returns stored variable from frame

        Check variable name's prefix and decides, which frame to look in for.
        Terminate program with ErrorCode.RUNTIME_NONEXIST_FRAME if frame is
        not initialized.
        Terminate program with ErrorCode.RUNTIME_UNDEF_VAR if variable was not
        defined within the frame.

        Parameters:
        var_name (str): Variable name

        Returs:
        Variable: Found Variable instance
        """
        simplified_name = Variable.simplify_var_name(var_name)
        var = None

        # get frame from variable prefix
        if var_name.startswith('GF@'):
            var = cls.global_frame.get_var(simplified_name)
        elif var_name.startswith('LF@'):
            if cls.local_frame is None:
                ErrorCode.exit_error(
                        f"Error while calling variable {var_name}\n"
                        "Local frame does not exists.",
                        ErrorCode.RUNTIME_NONEXIST_FRAME)
            var = cls.local_frame.get_var(simplified_name)
        else:
            if cls.temp_frame is None or not cls.temp_frame.is_active:
                ErrorCode.exit_error(
                        f"Error while calling variable {var_name}\n"
                        "Temporary frame does not exists.",
                        ErrorCode.RUNTIME_NONEXIST_FRAME)
            var = cls.temp_frame.get_var(simplified_name)

        if var is None:
            ErrorCode.exit_error(
                f"Error: Variable {var_name} has not been defined",
                ErrorCode.RUNTIME_UNDEF_VAR)
        return var
            

    @classmethod
    def get_symbol(cls, argument: Argument) -> Argument:
        """Return a symbol (variable or constant) from argument

        Parameters:
        argument (Argument): Instance of argument

        Returns:
        Argument: Extracted symbol from argument (variable or constant)
        """
        if argument.type == 'var':
            var: Variable = cls.get_variable(argument.value)
            return var
        return argument

    @classmethod
    def get_line(cls) -> str:
        """Return read data from stdin or input file

        Returns:
        str: Read data

        """
        if cls.input_file is None:
            try:
                return input()
            except:
                return None

        # reading from the file
        # file content is stored in list, last item is EOF
        # increase line counter when new line read
        if cls._line_index < len(cls.input_file):
            ret = cls.input_file[cls._line_index]
            cls._line_index += 1
            return ret
        return None


    @classmethod
    def set_jumps(cls, lof_ins: list):
        """Set jump destinations to labels

        Search for LABEL instruction in sorted list of instructions and create
        new {key: value} relationship of {label_name, index_of_instruction}.

        Parameters:
        lof_ins (list): List of instructions (Statement) extracted from XML file

        """
        for i in range(len(lof_ins)):
            stat = lof_ins[i]
            if stat.ins == 'LABEL':
                # jump one forward (instruction after label)
                cls.labels[stat.args[0].value] = i+1

    @classmethod
    def update_label_data(cls, stat: Statement):
        """Update label-instruction related data

        Parameters:
        stat (Statement): Processing instruction

        """
        if stat.ins == 'LABEL':
            label_name = stat.args[0].value
            if cls.labels.get(label_name) is not None:
                sys.exit(ErrorCode.SEMANTIC_ERROR)
            cls.labels[label_name] = 0

            # remove from undefined label if exists
            if label_name in cls.undef_labels:
                cls.undef_labels.remove(label_name)

        elif stat.ins in ('JUMP', 'JUMPIFEQ', 'JUMPIFNEQ', 'CALL'):
            # add label to undefined label if label doesn't exists yet
            if cls.labels.get(stat.args[0].value) is None:
                cls.undef_labels.add(stat.args[0].value)

    @classmethod
    def stack_push(cls, value):
        """Push value to the data stack

        Parameters:
        value (any): Constant value

        """
        cls.stack_vals.append(value)

    @classmethod
    def stack_pop(cls):
        """Pop value from the data stack

        Terminate program with ErrorCode.RUNTIME_MISSING_VALUE when
        stack is empty.

        Returns:
        Variable: Value from stack stored in temporary value

        """
        if len(cls.stack_vals) < 1:
            ErrorCode.exit_error("Stack is empty", ErrorCode.RUNTIME_MISSING_VALUE)
        temp_var = Variable()
        temp_var.value = cls.stack_vals.pop()
        return temp_var
