"""Definition of instruction set of IPPcode22 (without stack operations)

All functions in this file take two parameters:
    prg_cntr (int): Value of current instruction pointer (program counter)
    args (list):     List of arguments of given command/statement

All functions return:
    int: Updated program counter

Author: Hung Do
File:   instruction_set.py
Module: proj2_module
"""
import re
import sys
from .error import ErrorCode
from .coredata import CoreData
from .frame import Frame, Variable
from .stack_instruction_set import *

def move(prg_cntr: int, args: list):
    """ Move value <symb> to <var>
        MOVE <var> <symb>
    """
    if len(args) != 2:
        ErrorCode.exit_error(
                f"""Wrong number of arguments while executing {prg_cntr+1}. command""",
                ErrorCode.XML_STRUCTURE_ERROR)

    var: Variable = CoreData.get_variable(args[0].value)
    op1 = CoreData.get_symbol(args[1])

    # initialization check
    if op1.type == 'UNDEF':
        ErrorCode.exit_error(
                f"Missing value while executing {prg_cntr+1}. command",
                ErrorCode.RUNTIME_MISSING_VALUE)

    var.value = op1.value
    return prg_cntr + 1


def createframe(prg_cntr: int, args: list):
    """ Creates temporary frame """
    if len(args) != 0:
        ErrorCode.exit_error(
                f"""Wrong number of arguments while executing {prg_cntr+1}. command""",
                ErrorCode.XML_STRUCTURE_ERROR)

    CoreData.temp_frame = Frame()
    return prg_cntr + 1


def pushframe(prg_cntr: int, args: list):
    """ Push temporary frame to stack of frames """
    if len(args) != 0:
        ErrorCode.exit_error(
                f"""Wrong number of arguments while executing {prg_cntr+1}. command""",
                ErrorCode.XML_STRUCTURE_ERROR)

    if CoreData.temp_frame is None or not CoreData.temp_frame.is_active:
        ErrorCode.exit_error(f"Cannot push non-existing frame at {prg_cntr+1}. command",
                             ErrorCode.RUNTIME_NONEXIST_FRAME)

    CoreData.stack_frames.append(CoreData.temp_frame)
    CoreData.temp_frame.is_active = False
    CoreData.local_frame = CoreData.temp_frame
    return prg_cntr + 1

def popframe(prg_cntr: int, args: list):
    """ Pop frame from stack of frames to temporary frame """
    if len(args) != 0:
        ErrorCode.exit_error(
                f"""Wrong number of arguments while executing {prg_cntr+1}. command""",
                ErrorCode.XML_STRUCTURE_ERROR)

    if len(CoreData.stack_frames) == 0:
        ErrorCode.exit_error(f"No frame to pop at {prg_cntr+1}. command",
                             ErrorCode.RUNTIME_NONEXIST_FRAME)

    CoreData.temp_frame = CoreData.stack_frames.pop()
    CoreData.temp_frame.is_active = True
    # set local frame
    if len(CoreData.stack_frames) == 0:
        # ErrorCode.exit_error(f"No frame to pop at {prg_cntr+1}. command",
        #                      ErrorCode.RUNTIME_NONEXIST_FRAME)
        CoreData.local_frame = None
    else:
        CoreData.local_frame = CoreData.stack_frames[-1]
    return prg_cntr + 1

def defvar(prg_cntr: int, args: list):
    """ Define new <var>
        DEFVAR <var>
    """
    if len(args) != 1:
        ErrorCode.exit_error(
                f"""Wrong number of arguments while executing {prg_cntr+1}. command""",
                ErrorCode.XML_STRUCTURE_ERROR)

    var_name = args[0].value
    CoreData.add_variable(var_name)
    return prg_cntr + 1

def call(prg_cntr: int, args: list):
    """ Jump to <label> while perserving instruction pointer value
        CALL <label>
    """
    if len(args) != 1:
        ErrorCode.exit_error(
                f"""Wrong number of arguments while executing {prg_cntr+1}. command""",
                ErrorCode.XML_STRUCTURE_ERROR)

    lbl_name = args[0].value
    # if CoreData.labels.get(lbl_name) is None:
    #     ErrorCode.exit_error(ErrorCode.SEMANTIC_ERROR)

    CoreData.stack_func.append(prg_cntr)
    return CoreData.labels[lbl_name] - 1

def return_i(prg_cntr: int, args: list):
    """ Jump back to stored instruction pointer value """
    if len(args) != 0:
        ErrorCode.exit_error(
                f"""Wrong number of arguments while executing {prg_cntr+1}. command""",
                ErrorCode.XML_STRUCTURE_ERROR)

    if len(CoreData.stack_func) == 0:
        ErrorCode.exit_error(
                f"""Return call from non-existing function while executing {prg_cntr+1}. command""",
                ErrorCode.RUNTIME_MISSING_VALUE)

    prg_cntr = CoreData.stack_func.pop()
    return prg_cntr + 1

def add(prg_cntr: int, args: list):
    """ Add two numbers and store in <var>
        ADD <var> <symb> <symb>
    """
    if len(args) != 3:
        ErrorCode.exit_error(
                f"""Wrong number of arguments while executing {prg_cntr+1}. command""",
                ErrorCode.XML_STRUCTURE_ERROR)

    var: Variable = CoreData.get_variable(args[0].value)
    op1 = CoreData.get_symbol(args[1])
    op2 = CoreData.get_symbol(args[2])

    # initialization check
    if op1.type == 'UNDEF' or op2.type == 'UNDEF':
        ErrorCode.exit_error(
                f"Missing value while executing {prg_cntr+1}. command",
                ErrorCode.RUNTIME_MISSING_VALUE)
    # runtime type check
    if (op1.type not in ('int', 'float') or op2.type not in ('int', 'float')
        or op1.type != op2.type):
        ErrorCode.exit_error(
                "Wrong symbol's data type while executing {prg_cntr+1}. command",
                ErrorCode.RUNTIME_WRONG_TYPE)

    var.value = op1.value + op2.value

    return prg_cntr + 1

def sub(prg_cntr: int, args: list):
    """ Subtract two numbers and store in <var>
        SUB <var> <symb> <symb>
    """
    if len(args) != 3:
        ErrorCode.exit_error(
                f"""Wrong number of arguments while executing {prg_cntr+1}. command""",
                ErrorCode.XML_STRUCTURE_ERROR)

    var: Variable = CoreData.get_variable(args[0].value)
    op1 = CoreData.get_symbol(args[1])
    op2 = CoreData.get_symbol(args[2])

    # initialization check
    if op1.type == 'UNDEF' or op2.type == 'UNDEF':
        ErrorCode.exit_error(
                f"Missing value while executing {prg_cntr+1}. command",
                ErrorCode.RUNTIME_MISSING_VALUE)
    # runtime type check
    if (op1.type not in ('int', 'float') or op2.type not in ('int', 'float')
        or op1.type != op2.type):
        ErrorCode.exit_error(
                "Wrong symbol's data type while executing {prg_cntr+1}. command",
                ErrorCode.RUNTIME_WRONG_TYPE)

    var.value = op1.value - op2.value
    return prg_cntr + 1

def mul(prg_cntr: int, args: list):
    """ Multiply two numbers and store in <var>
        MUL <var> <symb> <symb>
    """
    if len(args) != 3:
        ErrorCode.exit_error(
                f"""Wrong number of arguments while executing {prg_cntr+1}. command""",
                ErrorCode.XML_STRUCTURE_ERROR)

    var: Variable = CoreData.get_variable(args[0].value)
    op1 = CoreData.get_symbol(args[1])
    op2 = CoreData.get_symbol(args[2])

    # initialization check
    if op1.type == 'UNDEF' or op2.type == 'UNDEF':
        ErrorCode.exit_error(
                f"Missing value while executing {prg_cntr+1}. command",
                ErrorCode.RUNTIME_MISSING_VALUE)
    # runtime type check
    if (op1.type not in ('int', 'float') or op2.type not in ('int', 'float')
        or op1.type != op2.type):
        ErrorCode.exit_error(
                "Wrong symbol's data type while executing {prg_cntr+1}. command",
                ErrorCode.RUNTIME_WRONG_TYPE)

    var.value = op1.value * op2.value
    return prg_cntr + 1

def div(prg_cntr: int, args: list):
    """ Divide two numbers and store in <var>
        DIV <var> <symb> <symb>
    """
    if len(args) != 3:
        ErrorCode.exit_error(
                f"""Wrong number of arguments while executing {prg_cntr+1}. command""",
                ErrorCode.XML_STRUCTURE_ERROR)

    var: Variable = CoreData.get_variable(args[0].value)
    op1 = CoreData.get_symbol(args[1])
    op2 = CoreData.get_symbol(args[2])

    # initialization check
    if op1.type == 'UNDEF' or op2.type == 'UNDEF':
        ErrorCode.exit_error(
                f"Missing value while executing {prg_cntr+1}. command",
                ErrorCode.RUNTIME_MISSING_VALUE)
    # runtime type check
    if (op1.type not in ('int', 'float') or op2.type not in ('int', 'float')
        or op1.type != op2.type):
        ErrorCode.exit_error(
                "Wrong symbol's data type while executing {prg_cntr+1}. command",
                ErrorCode.RUNTIME_WRONG_TYPE)

    # div zero check
    if op2.value == 0:
        ErrorCode.exit_error(f"Cannot divide by zero at {prg_cntr+1}. command",
                             ErrorCode.RUNTIME_WRONG_VALUE)

    var.value = op1.value / op2.value
    return prg_cntr + 1

def idiv(prg_cntr: int, args: list):
    """ Divide two numbers and store in <var> round down value
        IDIV <var> <symb> <symb>
    """
    if len(args) != 3:
        ErrorCode.exit_error(
                f"""Wrong number of arguments while executing {prg_cntr+1}. command""",
                ErrorCode.XML_STRUCTURE_ERROR)

    var: Variable = CoreData.get_variable(args[0].value)
    op1 = CoreData.get_symbol(args[1])
    op2 = CoreData.get_symbol(args[2])

    # initialization check
    if op1.type == 'UNDEF' or op2.type == 'UNDEF':
        ErrorCode.exit_error(
                f"Missing value while executing {prg_cntr+1}. command",
                ErrorCode.RUNTIME_MISSING_VALUE)
    # runtime type check
    if (op1.type not in ('int', 'float') or op2.type not in ('int', 'float')
        or op1.type != op2.type):
        ErrorCode.exit_error(
                "Wrong symbol's data type while executing {prg_cntr+1}. command",
                ErrorCode.RUNTIME_WRONG_TYPE)

    # div zero check
    if op2.value == 0:
        ErrorCode.exit_error(f"Cannot divide by zero at {prg_cntr+1}. command",
                             ErrorCode.RUNTIME_WRONG_VALUE)

    var.value = op1.value // op2.value
    return prg_cntr + 1

def lt(prg_cntr: int, args: list):
    """ Check if <symb1> is less than <symb2>; store in <var>
        LT <var> <symb1> <symb2>
    """
    if len(args) != 3:
        ErrorCode.exit_error(
                f"""Wrong number of arguments while executing {prg_cntr+1}. command""",
                ErrorCode.XML_STRUCTURE_ERROR)

    var: Variable = CoreData.get_variable(args[0].value)
    op1 = CoreData.get_symbol(args[1])
    op2 = CoreData.get_symbol(args[2])

    # initialization check
    if op1.type == 'UNDEF' or op2.type == 'UNDEF':
        ErrorCode.exit_error(
                f"Missing value while executing {prg_cntr+1}. command",
                ErrorCode.RUNTIME_MISSING_VALUE)
    # runtime type check
    if op1.type == 'nil' or op2.type == 'nil':
        ErrorCode.exit_error(
                "Wrong symbol's data type while executing {prg_cntr+1}. command",
                ErrorCode.RUNTIME_WRONG_TYPE)
    if op1.type != op2.type:
        ErrorCode.exit_error(
                "Wrong symbol's data type while executing {prg_cntr+1}. command",
                ErrorCode.RUNTIME_WRONG_TYPE)

    var.value = op1.value < op2.value
    return prg_cntr + 1

def gt(prg_cntr: int, args: list):
    """ Check if <symb1> is greater than <symb2>; store in <var>
        GT <var> <symb1> <symb2>
    """
    if len(args) != 3:
        ErrorCode.exit_error(
                f"""Wrong number of arguments while executing {prg_cntr+1}. command""",
                ErrorCode.XML_STRUCTURE_ERROR)

    var: Variable = CoreData.get_variable(args[0].value)
    op1 = CoreData.get_symbol(args[1])
    op2 = CoreData.get_symbol(args[2])

    # initialization check
    if op1.type == 'UNDEF' or op2.type == 'UNDEF':
        ErrorCode.exit_error(
                f"Missing value while executing {prg_cntr+1}. command",
                ErrorCode.RUNTIME_MISSING_VALUE)
    # runtime type check
    if op1.type == 'nil' or op2.type == 'nil' or op1.type != op2.type:
        ErrorCode.exit_error(
                "Wrong symbol's data type while executing {prg_cntr+1}. command",
                ErrorCode.RUNTIME_WRONG_TYPE)

    var.value = op1.value > op2.value
    return prg_cntr + 1

def eq(prg_cntr: int, args: list):
    """ Check if <symb1> and <symb2> values are equal; store in <var>
        EQ <var> <symb1> <symb2>
    """
    if len(args) != 3:
        ErrorCode.exit_error(
                f"""Wrong number of arguments while executing {prg_cntr+1}. command""",
                ErrorCode.XML_STRUCTURE_ERROR)

    var: Variable = CoreData.get_variable(args[0].value)
    op1 = CoreData.get_symbol(args[1])
    op2 = CoreData.get_symbol(args[2])

    # initialization check
    if op1.type == 'UNDEF' or op2.type == 'UNDEF':
        ErrorCode.exit_error(
                f"Missing value while executing {prg_cntr+1}. command",
                ErrorCode.RUNTIME_MISSING_VALUE)
    # runtime type check
    if op1.type != op2.type and op1.type != 'nil' and op2.type != 'nil':
        ErrorCode.exit_error(
                "Wrong symbol's data type while executing {prg_cntr+1}. command",
                ErrorCode.RUNTIME_WRONG_TYPE)

    var.value = op1.value == op2.value
    return prg_cntr + 1

def and_i(prg_cntr: int, args: list):
    """ Store 'true' in <var> if both <symb1> and <symb2> are 'true'
            otherwise store 'false'
        AND <var> <symb1> <symb2>
    """
    if len(args) != 3:
        ErrorCode.exit_error(
                f"""Wrong number of arguments while executing {prg_cntr+1}. command""",
                ErrorCode.XML_STRUCTURE_ERROR)

    var: Variable = CoreData.get_variable(args[0].value)
    op1 = CoreData.get_symbol(args[1])
    op2 = CoreData.get_symbol(args[2])

    # initialization check
    if op1.type == 'UNDEF' or op2.type == 'UNDEF':
        ErrorCode.exit_error(
                f"Missing value while executing {prg_cntr+1}. command",
                ErrorCode.RUNTIME_MISSING_VALUE)
    # runtime type check
    if op1.type != 'bool' or op2.type != 'bool':
        ErrorCode.exit_error(
                "Wrong symbol's data type while executing {prg_cntr+1}. command",
                ErrorCode.RUNTIME_WRONG_TYPE)

    var.value = op1.value and op2.value
    return prg_cntr + 1

def or_i(prg_cntr: int, args: list):
    """ Store 'false' in <var> if both <symb1> and <symb2> are 'false'
            otherwise store 'true'
        OR <var> <symb1> <symb2>
    """
    if len(args) != 3:
        ErrorCode.exit_error(
                f"""Wrong number of arguments while executing {prg_cntr+1}. command""",
                ErrorCode.XML_STRUCTURE_ERROR)

    var: Variable = CoreData.get_variable(args[0].value)
    op1 = CoreData.get_symbol(args[1])
    op2 = CoreData.get_symbol(args[2])

    # initialization check
    if op1.type == 'UNDEF' or op2.type == 'UNDEF':
        ErrorCode.exit_error(
                f"Missing value while executing {prg_cntr+1}. command",
                ErrorCode.RUNTIME_MISSING_VALUE)
    # runtime type check
    if op1.type != 'bool' or op2.type != 'bool':
        ErrorCode.exit_error(
                "Wrong symbol's data type while executing {prg_cntr+1}. command",
                ErrorCode.RUNTIME_WRONG_TYPE)

    var.value = op1.value or op2.value
    return prg_cntr + 1

def not_i(prg_cntr: int, args: list):
    """ Negate <symb> value and store in <var>
        NOT <var> <symb>
    """
    if len(args) != 2:
        ErrorCode.exit_error(
                f"""Wrong number of arguments while executing {prg_cntr+1}. command""",
                ErrorCode.XML_STRUCTURE_ERROR)

    var: Variable = CoreData.get_variable(args[0].value)
    op1 = CoreData.get_symbol(args[1])

    # initialization check
    if op1.type == 'UNDEF':
        ErrorCode.exit_error(
                f"Missing value while executing {prg_cntr+1}. command",
                ErrorCode.RUNTIME_MISSING_VALUE)
    # runtime type check
    if op1.type != 'bool':
        ErrorCode.exit_error(
                "Wrong symbol's data type while executing {prg_cntr+1}. command",
                ErrorCode.RUNTIME_WRONG_TYPE)

    var.value = not op1.value
    return prg_cntr + 1

def int2char(prg_cntr: int, args: list):
    """ Convert number <symb> to ascii value character
        INT2CHAR <var> <symb>
    """
    if len(args) != 2:
        ErrorCode.exit_error(
                f"""Wrong number of arguments while executing {prg_cntr+1}. command""",
                ErrorCode.XML_STRUCTURE_ERROR)

    var: Variable = CoreData.get_variable(args[0].value)
    op1 = CoreData.get_symbol(args[1])

    # initialization check
    if op1.type == 'UNDEF':
        ErrorCode.exit_error(
                f"Missing value while executing {prg_cntr+1}. command",
                ErrorCode.RUNTIME_MISSING_VALUE)
    # runtime type check
    if op1.type != 'int':
        ErrorCode.exit_error(
                "Wrong symbol's data type while executing {prg_cntr+1}. command",
                ErrorCode.RUNTIME_WRONG_TYPE)

    # ord function range check
    if op1.value not in range(UNICODE_MAX_VAL + 1):
        ErrorCode.exit_error("Wrong string handling while executing {prg_cntr+1}. command",
                             ErrorCode.RUNTIME_STRING_HANDLING)

    var.value = chr(op1.value)
    return prg_cntr + 1

def stri2int(prg_cntr: int, args: list):
    """ Store ascii value of character at position <symb2> in string <symb1>
            in <var>
        STRI2INT <var> <symb1> <symb2>
    """
    if len(args) != 3:
        ErrorCode.exit_error(
                f"""Wrong number of arguments while executing {prg_cntr+1}. command""",
                ErrorCode.XML_STRUCTURE_ERROR)

    var: Variable = CoreData.get_variable(args[0].value)
    op1 = CoreData.get_symbol(args[1])
    op2 = CoreData.get_symbol(args[2])

    # initialization check
    if op1.type == 'UNDEF' or op2.type == 'UNDEF':
        ErrorCode.exit_error(
                f"Missing value while executing {prg_cntr+1}. command",
                ErrorCode.RUNTIME_MISSING_VALUE)
    # runtime type check
    if op1.type != 'string' or op2.type != 'int':
        ErrorCode.exit_error(
                "Wrong symbol's data type while executing {prg_cntr+1}. command",
                ErrorCode.RUNTIME_WRONG_TYPE)

    # index range check
    if op2.value not in range(len(op1.value)):
        ErrorCode.exit_error("Wrong string handling while executing {prg_cntr+1}. command",
                             ErrorCode.RUNTIME_STRING_HANDLING)

    var.value = ord(op1.value[op2.value])
    return prg_cntr + 1

def int2float(prg_cntr: int, args: list):
    """ Converts int value <symb> to float and store in <var>
        INT2FLOAT <var> <symb>
    """
    if len(args) != 2:
        ErrorCode.exit_error(
                f"""Wrong number of arguments while executing {prg_cntr+1}. command""",
                ErrorCode.XML_STRUCTURE_ERROR)

    var: Variable = CoreData.get_variable(args[0].value)
    op1 = CoreData.get_symbol(args[1])

    # initialization check
    if op1.type == 'UNDEF':
        ErrorCode.exit_error(
                f"Missing value while executing {prg_cntr+1}. command",
                ErrorCode.RUNTIME_MISSING_VALUE)
    # runtime type check
    if op1.type != 'int':
        ErrorCode.exit_error(
                "Wrong symbol's data type while executing {prg_cntr+1}. command",
                ErrorCode.RUNTIME_WRONG_TYPE)

    var.value = float(op1.value)
    return prg_cntr + 1

def float2int(prg_cntr: int, args: list):
    """ Converts float value <symb> to int and store in <var>
        FLOAT2INT <var> <symb>
    """
    if len(args) != 2:
        ErrorCode.exit_error(
                f"""Wrong number of arguments while executing {prg_cntr+1}. command""",
                ErrorCode.XML_STRUCTURE_ERROR)

    var: Variable = CoreData.get_variable(args[0].value)
    op1 = CoreData.get_symbol(args[1])

    # initialization check
    if op1.type == 'UNDEF':
        ErrorCode.exit_error(
                f"Missing value while executing {prg_cntr+1}. command",
                ErrorCode.RUNTIME_MISSING_VALUE)
    # runtime type check
    if op1.type != 'float':
        ErrorCode.exit_error(
                "Wrong symbol's data type while executing {prg_cntr+1}. command",
                ErrorCode.RUNTIME_WRONG_TYPE)

    var.value = int(op1.value)
    return prg_cntr + 1

def read(prg_cntr: int, args: list):
    """ Read from input file <type> and store in <var>
        READ <var> <type>
    """
    if len(args) != 2:
        ErrorCode.exit_error(
                f"""Wrong number of arguments while executing {prg_cntr+1}. command""",
                ErrorCode.XML_STRUCTURE_ERROR)

    var: Variable = CoreData.get_variable(args[0].value)

    # data type
    op1 = CoreData.get_symbol(args[1])
    input_value = CoreData.get_line()

    if op1.value == 'string':
        var.value = input_value
    elif op1.value == 'bool':
        var.value = (input_value.lower() == 'true')
    elif op1.value == 'int':
        try:
            var.value = int(input_value)
        except:
            var.value = None
    elif op1.value == 'float':
        try:
            if re.match(CoreData.REG_TYPE['float_hex'], input_value):
                var.value = float.fromhex(input_value)
            else:
                var.value = float(input_value)
        except:
            var.value = None
    else:
        ErrorCode.exit_error(
                f"Error while reading input at {prg_cntr+1}. command",
                ErrorCode.RUNTIME_WRONG_VALUE)

    return prg_cntr + 1

def write(prg_cntr: int, args: list):
    """ Write to STDIN <symb> value
        WRITE <symb>
    """
    if len(args) != 1:
        ErrorCode.exit_error(
                f"""Wrong number of arguments while executing {prg_cntr+1}. command""",
                ErrorCode.XML_STRUCTURE_ERROR)

    symb = CoreData.get_symbol(args[0])

    if symb.type == 'UNDEF':
        ErrorCode.exit_error(
                f"Missing value while executing {prg_cntr+1}. command",
                ErrorCode.RUNTIME_MISSING_VALUE)

    if symb.type == 'nil':
        print('', end='', flush=True)
    elif symb.type == 'bool':
        output_msg = 'true' if symb.value else 'false'
        print(output_msg, end='', flush=True)
    elif symb.type == 'float':
        print(float.hex(symb.value), end='', flush=True)
    else:
        print(symb.value, end='', flush=True)
    return prg_cntr + 1

def concat(prg_cntr: int, args: list):
    """ Concatenate <symb2> to <symb1>; store in <var>
        CONCAR <var> <symb1> <symb2>
    """
    if len(args) != 3:
        ErrorCode.exit_error(
                f"""Wrong number of arguments while executing {prg_cntr+1}. command""",
                ErrorCode.XML_STRUCTURE_ERROR)

    var: Variable = CoreData.get_variable(args[0].value)
    op1 = CoreData.get_symbol(args[1])
    op2 = CoreData.get_symbol(args[2])

    # initialization check
    if op1.type == 'UNDEF' or op2.type == 'UNDEF':
        ErrorCode.exit_error(
                f"Missing value while executing {prg_cntr+1}. command",
                ErrorCode.RUNTIME_MISSING_VALUE)
    # runtime type check
    if op1.type != 'string' or op2.type != 'string':
        ErrorCode.exit_error(
                "Wrong symbol's data type while executing {prg_cntr+1}. command",
                ErrorCode.RUNTIME_WRONG_TYPE)

    var.value = op1.value + op2.value
    return prg_cntr + 1

def strlen(prg_cntr: int, args: list):
    """ Store string length of <symb> in <var>
        STRLEN <var> <symb>
    """
    if len(args) != 2:
        ErrorCode.exit_error(
                f"""Wrong number of arguments while executing {prg_cntr+1}. command""",
                ErrorCode.XML_STRUCTURE_ERROR)

    var: Variable = CoreData.get_variable(args[0].value)
    op1 = CoreData.get_symbol(args[1])

    # initialization check
    if op1.type == 'UNDEF':
        ErrorCode.exit_error(
                f"Missing value while executing {prg_cntr+1}. command",
                ErrorCode.RUNTIME_MISSING_VALUE)
    # runtime type check
    if op1.type != 'string':
        ErrorCode.exit_error(
                "Wrong symbol's data type while executing {prg_cntr+1}. command",
                ErrorCode.RUNTIME_WRONG_TYPE)

    var.value = len(op1.value)
    return prg_cntr + 1

def getchar(prg_cntr: int, args: list):
    """ Get character of <symb1> at position <symb2>; store in <var>
        GETCHAR <var> <symb1> <symb2>
    """
    if len(args) != 3:
        ErrorCode.exit_error(
                f"""Wrong number of arguments while executing {prg_cntr+1}. command""",
                ErrorCode.XML_STRUCTURE_ERROR)

    var: Variable = CoreData.get_variable(args[0].value)
    op1 = CoreData.get_symbol(args[1])
    op2 = CoreData.get_symbol(args[2])

    # initialization check
    if op1.type == 'UNDEF' or op2.type == 'UNDEF':
        ErrorCode.exit_error(
                f"Missing value while executing {prg_cntr+1}. command",
                ErrorCode.RUNTIME_MISSING_VALUE)
    # runtime type check
    if op1.type != 'string' or op2.type != 'int':
        ErrorCode.exit_error(
                "Wrong symbol's data type while executing {prg_cntr+1}. command",
                ErrorCode.RUNTIME_WRONG_TYPE)

    # index range check
    if op2.value not in range(len(op1.value)):
        ErrorCode.exit_error("Wrong string handling while executing {prg_cntr+1}. command",
                             ErrorCode.RUNTIME_STRING_HANDLING)

    var.value = op1.value[op2.value]
    return prg_cntr + 1

def setchar(prg_cntr: int, args: list):
    """ Set character of <symb1> at position <symb2>; store in <var>
        SETCHAR <var> <symb1> <symb2>
    """
    if len(args) != 3:
        ErrorCode.exit_error(
                f"""Wrong number of arguments while executing {prg_cntr+1}. command""",
                ErrorCode.XML_STRUCTURE_ERROR)

    var: Variable = CoreData.get_variable(args[0].value)
    op1 = CoreData.get_symbol(args[1])
    op2 = CoreData.get_symbol(args[2])

    # initialization check
    if var.type == 'UNDEF' or op1.type == 'UNDEF' or op2.type == 'UNDEF':
        ErrorCode.exit_error(
                f"Missing value while executing {prg_cntr+1}. command",
                ErrorCode.RUNTIME_MISSING_VALUE)
    # runtime type check
    if var.type != 'string' or op1.type != 'int' or op2.type != 'string':
        ErrorCode.exit_error(
                "Wrong symbol's data type while executing {prg_cntr+1}. command",
                ErrorCode.RUNTIME_WRONG_TYPE)

    # index range check
    if op1.value not in range(len(var.value)) or len(op2.value) == 0:
        ErrorCode.exit_error("Wrong string handling while executing {prg_cntr+1}. command",
                             ErrorCode.RUNTIME_STRING_HANDLING)

    # ----- setchar ------
    new_char = op2.value[0]
    new_str  = list(var.value)
    new_str[op1.value] = new_char
    var.value = ''.join(new_str)
    # --------------------
    return prg_cntr + 1

def type_i(prg_cntr: int, args: list):
    """ Store type of <symb> in string form in <var>
        TYPE <var> <symb>
    """
    if len(args) != 2:
        ErrorCode.exit_error(
                f"""Wrong number of arguments while executing {prg_cntr+1}. command""",
                ErrorCode.XML_STRUCTURE_ERROR)

    var: Variable = CoreData.get_variable(args[0].value)
    op1 = CoreData.get_symbol(args[1])

    # runtime type check
    if op1.type == 'UNDEF':
        var.value = ''
    else:
        var.value = op1.type
    return prg_cntr + 1

def label(prg_cntr: int, args: list):
    """ Label to jump
        LABEL <label>
    """
    if len(args) != 1:
        ErrorCode.exit_error(
                f"""Wrong number of arguments while executing {prg_cntr+1}. command""",
                ErrorCode.XML_STRUCTURE_ERROR)

    return prg_cntr + 1

def jump(prg_cntr: int, args: list):
    """ Jump to <label>
        JUMP <label>
    """
    if len(args) != 1:
        ErrorCode.exit_error(
                f"""Wrong number of arguments while executing {prg_cntr+1}. command""",
                ErrorCode.XML_STRUCTURE_ERROR)

    lbl_name = args[0].value

    return CoreData.labels[lbl_name]

def jumpifeq(prg_cntr: int, args: list):
    """ Jump to <label> if <symb1> is equal to <symb2>
        JUMPIFEQ <label> <symb1> <sym2>
    """
    if len(args) != 3:
        ErrorCode.exit_error(
                f"""Wrong number of arguments while executing {prg_cntr+1}. command""",
                ErrorCode.XML_STRUCTURE_ERROR)

    lbl_name = args[0].value
    op1 = CoreData.get_symbol(args[1])
    op2 = CoreData.get_symbol(args[2])

    # initialization check
    if op1.type == 'UNDEF' or op2.type == 'UNDEF':
        ErrorCode.exit_error(
                f"Missing value while executing {prg_cntr+1}. command",
                ErrorCode.RUNTIME_MISSING_VALUE)

    # runtime type check
    if op1.type != op2.type and op1.type != 'nil' and op2.type != 'nil':
        ErrorCode.exit_error(
                "Wrong symbol's data type while executing {prg_cntr+1}. command",
                ErrorCode.RUNTIME_WRONG_TYPE)

    return CoreData.labels[lbl_name] if op1.value == op2.value else prg_cntr+1

def jumpifneq(prg_cntr: int, args: list):
    """ Jump to <label> if <symb1> is not equal to <symb2>
        JUMPIFNEQ <label> <symb1> <sym2>
    """
    if len(args) != 3:
        ErrorCode.exit_error(
                f"""Wrong number of arguments while executing {prg_cntr+1}. command""",
                ErrorCode.XML_STRUCTURE_ERROR)

    lbl_name = args[0].value
    op1 = CoreData.get_symbol(args[1])
    op2 = CoreData.get_symbol(args[2])

    # initialization check
    if op1.type == 'UNDEF' or op2.type == 'UNDEF':
        ErrorCode.exit_error(
                f"Missing value while executing {prg_cntr+1}. command",
                ErrorCode.RUNTIME_MISSING_VALUE)

    # runtime type check
    if op1.type != op2.type and op1.type != 'nil' and op2.type != 'nil':
        ErrorCode.exit_error(
                "Wrong symbol's data type while executing {prg_cntr+1}. command",
                ErrorCode.RUNTIME_WRONG_TYPE)

    return CoreData.labels[lbl_name] if op1.value != op2.value else prg_cntr+1

def exit_i(prg_cntr: int, args: list):
    """ Exit program with <symb> value
        EXIT <symb>
    """
    if len(args) != 1:
        ErrorCode.exit_error(
                f"""Wrong number of arguments while executing {prg_cntr+1}. command""",
                ErrorCode.XML_STRUCTURE_ERROR)

    symb  = CoreData.get_symbol(args[0])

    # initialization check
    if symb.type == 'UNDEF':
        ErrorCode.exit_error(
                f"Missing value while executing {prg_cntr+1}. command",
                ErrorCode.RUNTIME_MISSING_VALUE)

    # runtime type check
    if symb.type != 'int':
        ErrorCode.exit_error(
                "Wrong symbol's data type while executing {prg_cntr+1}. command",
                ErrorCode.RUNTIME_WRONG_TYPE)

    # value range check
    if symb.value not in range(50):
        ErrorCode.exit_error("Error: expexted output value in range (0-49)",
                             ErrorCode.RUNTIME_WRONG_VALUE)

    # dead code
    sys.exit(symb.value)

def dprint(prg_cntr: int, args: list):
    """ Write <symb> value to STDERR
        DPRINT <symb>
    """
    if len(args) != 1:
        ErrorCode.exit_error(
                f"""Wrong number of arguments while executing {prg_cntr+1}. command""",
                ErrorCode.XML_STRUCTURE_ERROR)

    symb = CoreData.get_symbol(args[0])

    # runtime type check
    if symb.type == 'UNDEF':
        ErrorCode.exit_error(
                f"Missing value while executing {prg_cntr+1}. command",
                ErrorCode.RUNTIME_MISSING_VALUE)

    if symb.type == 'nil':
        sys.stderr.write('')
    elif symb.type == 'bool':
        output_msg = 'true' if symb.value else 'false'
        sys.stderr.write(output_msg)
    else:
        sys.stderr.write(symb.value)
    return prg_cntr + 1

def break_i(prg_cntr: int, args: list):
    """ Write program debug information to STDERR
        BREAK
    """
    if len(args) != 0:
        ErrorCode.exit_error(
                f"""Wrong number of arguments while executing {prg_cntr+1}. command""",
                ErrorCode.XML_STRUCTURE_ERROR)
    sys.stderr.write("================================\n")
    sys.stderr.write(f"Pozice v kodu: {prg_cntr + 1}. \n")

    # item[0] -> var name
    # item[1] -> var value
    sys.stderr.write("\nObsah globalniho ramce: \n")
    for item in CoreData.global_frame.vars.items():
        sys.stderr.write(f"\t{item[0]}: {item[1]}\n")

    sys.stderr.write("\nObsah lokalniho ramce: \n")
    for item in CoreData.local_frame.vars.items():
        sys.stderr.write(f"\t{item[0]}: {item[1]}\n")

    sys.stderr.write("\nObsah docasneho ramce: \n")
    if CoreData.temp_frame is None or not CoreData.temp_frame.is_active:
        sys.stderr.write("\tDocasny ramec je zatim nedefinovany\n\n")
    else:
        for item in CoreData.temp_frame.vars.items():
            sys.stderr.write(f"\t{item[0]}: {item[1]}\n")

    sys.stderr.write(f"Pocet vykonanych instrukci: {CoreData.ins_performed}\n")
    sys.stderr.write("================================\n")

    return prg_cntr + 1

instruct_set = {
        'MOVE': move,
        'CREATEFRAME': createframe,
        'PUSHFRAME': pushframe,
        'POPFRAME': popframe,
        'DEFVAR': defvar,
        'CALL': call,
        'RETURN': return_i,
        'PUSHS': pushs,
        'CLEARS': clears,
        'POPS': pops,
        'ADD': add,
        'SUB': sub,
        'MUL': mul,
        'DIV': div,
        'IDIV': idiv,
        'LT': lt,
        'GT': gt,
        'EQ': eq,
        'AND': and_i,
        'OR': or_i,
        'NOT': not_i,
        'INT2CHAR': int2char,
        'STRI2INT': stri2int,
        'INT2FLOAT': int2float,
        'FLOAT2INT': float2int,
        'READ': read,
        'WRITE': write,
        'CONCAT': concat,
        'STRLEN': strlen,
        'GETCHAR': getchar,
        'SETCHAR': setchar,
        'TYPE': type_i,
        'LABEL': label,
        'JUMP': jump,
        'JUMPIFEQ': jumpifeq,
        'JUMPIFNEQ': jumpifneq,
        'EXIT': exit_i,
        'DPRINT': dprint,
        'BREAK': break_i,

        'ADDS': adds,
        'SUBS': subs,
        'MULS': muls,
        'DIVS': divs,
        'IDIVS': idivs,
        'LTS': lts,
        'GTS': gts,
        'EQS': eqs,
        'ANDS': ands,
        'ORS': ors,
        'NOTS': nots,
        'INT2CHARS': int2chars,
        'STRI2INTS': stri2ints,
        'INT2FLOATS': int2floats,
        'FLOAT2INTS': float2ints,
        'JUMPIFEQS': jumpifeqs,
        'JUMPIFNEQS': jumpifneqs,
        }
