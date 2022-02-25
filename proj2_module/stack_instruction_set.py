"""Instruction set of stack operations

All functions in this file take two parameters:
    prg_cntr (int): Value of current instruction pointer (program counter)
    args (list):     List of arguments of given command/statement

All functions return:
    int: Updated program counter

Author: Hung Do
File:   stack_instruction_set.py
Module: proj2_module
"""
from .error import ErrorCode
from .coredata import CoreData
from .statement import Argument
from .frame import Variable

UNICODE_MAX_VAL: int = 1_114_111

def pushs(prg_cntr: int, args: list):
    """ Push value of <symb> to stack
        PUSHS <symb>
    """
    if len(args) != 1:
        ErrorCode.exit_error(
                f"""Wrong number of arguments while executing {prg_cntr+1}. command""",
                ErrorCode.XML_STRUCTURE_ERROR)

    if args[0].type == 'var':
        var = CoreData.get_variable(args[0].value)
        if var.type == 'UNDEF':
            ErrorCode.exit_error(
                    f"Missing value while executing {prg_cntr+1}. command",
                    ErrorCode.RUNTIME_MISSING_VALUE)
        value = var.value
    else:
        value = args[0].value

    CoreData.stack_push(value)
    return prg_cntr + 1

def pops(prg_cntr: int, args: list):
    """ Pop data from stack to <var>
        POPS <var>
    """
    if len(args) != 1:
        ErrorCode.exit_error(
                f"""Wrong number of arguments while executing {prg_cntr+1}. command""",
                ErrorCode.XML_STRUCTURE_ERROR)

    var: Variable = CoreData.get_variable(args[0].value)

    stack_value = CoreData.stack_pop()
    var.value = stack_value.value
    return prg_cntr + 1

def clears(prg_cntr: int, args: list):
    if len(args) != 0:
        ErrorCode.exit_error(
                f"""Wrong number of arguments while executing {prg_cntr+1}. command""",
                ErrorCode.XML_STRUCTURE_ERROR)
    CoreData.stack_vals.clear()
    return prg_cntr + 1

def adds(prg_cntr: int, args: list):
    """ Add two numbers and store in <var>
        ADDS
    """
    if len(args) != 0:
        ErrorCode.exit_error(
                f"""Wrong number of arguments while executing {prg_cntr+1}. command""",
                ErrorCode.XML_STRUCTURE_ERROR)

    op2 = CoreData.stack_pop()
    op1 = CoreData.stack_pop()

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

    CoreData.stack_push(op1.value + op2.value)
    return prg_cntr + 1

def subs(prg_cntr: int, args: list):
    """ Subtract two numbers and store in <var>
        SUBS
    """
    if len(args) != 0:
        ErrorCode.exit_error(
                f"""Wrong number of arguments while executing {prg_cntr+1}. command""",
                ErrorCode.XML_STRUCTURE_ERROR)

    op2 = CoreData.stack_pop()
    op1 = CoreData.stack_pop()

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

    CoreData.stack_push(op1.value - op2.value)
    return prg_cntr + 1

def muls(prg_cntr: int, args: list):
    """ Multiply two numbers and store in <var>
        MULS
    """
    if len(args) != 0:
        ErrorCode.exit_error(
                f"""Wrong number of arguments while executing {prg_cntr+1}. command""",
                ErrorCode.XML_STRUCTURE_ERROR)

    op2 = CoreData.stack_pop()
    op1 = CoreData.stack_pop()

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

    CoreData.stack_push(op1.value * op2.value)
    return prg_cntr + 1

def divs(prg_cntr: int, args: list):
    """ Divide two numbers and store in <var>
        DIVS
    """
    if len(args) != 0:
        ErrorCode.exit_error(
                f"""Wrong number of arguments while executing {prg_cntr+1}. command""",
                ErrorCode.XML_STRUCTURE_ERROR)

    op2 = CoreData.stack_pop()
    op1 = CoreData.stack_pop()

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
        ErrorCode.exit_error(
                "Cannot divide by zero!",
                ErrorCode.RUNTIME_WRONG_VALUE)

    CoreData.stack_push(op1.value / op2.value)
    return prg_cntr + 1

def idivs(prg_cntr: int, args: list):
    """ Divide two numbers and store in <var> round down value
        IDIVS
    """
    if len(args) != 0:
        ErrorCode.exit_error(
                f"""Wrong number of arguments while executing {prg_cntr+1}. command""",
                ErrorCode.XML_STRUCTURE_ERROR)

    op2 = CoreData.stack_pop()
    op1 = CoreData.stack_pop()

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
        ErrorCode.exit_error(
                "Cannot divide by zero!",
                ErrorCode.RUNTIME_WRONG_VALUE)

    CoreData.stack_push(op1.value // op2.value)
    return prg_cntr + 1

def lts(prg_cntr: int, args: list):
    """ Check if <symb1> is less than <symb2>; store in <var>
        LTS
    """
    if len(args) != 0:
        ErrorCode.exit_error(
                f"""Wrong number of arguments while executing {prg_cntr+1}. command""",
                ErrorCode.XML_STRUCTURE_ERROR)

    op2 = CoreData.stack_pop()
    op1 = CoreData.stack_pop()

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

    CoreData.stack_push(op1.value < op2.value)
    return prg_cntr + 1

def gts(prg_cntr: int, args: list):
    """ Check if <symb1> is greater than <symb2>; store in <var>
        GTS
    """
    if len(args) != 0:
        ErrorCode.exit_error(
                f"""Wrong number of arguments while executing {prg_cntr+1}. command""",
                ErrorCode.XML_STRUCTURE_ERROR)

    op2 = CoreData.stack_pop()
    op1 = CoreData.stack_pop()

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

    # value = op1.value < op2.value
    CoreData.stack_push(op1.value > op2.value)
    return prg_cntr + 1

def eqs(prg_cntr: int, args: list):
    """ Check if <symb1> and <symb2> values are equal; store in <var>
        EQS
    """
    if len(args) != 0:
        ErrorCode.exit_error(
                f"""Wrong number of arguments while executing {prg_cntr+1}. command""",
                ErrorCode.XML_STRUCTURE_ERROR)

    op2 = CoreData.stack_pop()
    op1 = CoreData.stack_pop()

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

    CoreData.stack_push(op1.value == op2.value)
    return prg_cntr + 1

def ands(prg_cntr: int, args: list):
    """ Store 'true' in <var> if both <symb1> and <symb2> are 'true'
            otherwise store 'false'
        ANDS
    """
    if len(args) != 0:
        ErrorCode.exit_error(
                f"""Wrong number of arguments while executing {prg_cntr+1}. command""",
                ErrorCode.XML_STRUCTURE_ERROR)

    op2 = CoreData.stack_pop()
    op1 = CoreData.stack_pop()

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

    CoreData.stack_push(op1.value and op2.value)
    return prg_cntr + 1

def ors(prg_cntr: int, args: list):
    """ Store 'false' in <var> if both <symb1> and <symb2> are 'false'
            otherwise store 'true'
        ORS
    """
    if len(args) != 0:
        ErrorCode.exit_error(
                f"""Wrong number of arguments while executing {prg_cntr+1}. command""",
                ErrorCode.XML_STRUCTURE_ERROR)

    op2 = CoreData.stack_pop()
    op1 = CoreData.stack_pop()

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

    CoreData.stack_push(op1.value or op2.value)
    return prg_cntr + 1

def nots(prg_cntr: int, args: list):
    """ Negate <symb> value and store in <var>
        NOTS
    """
    if len(args) != 0:
        ErrorCode.exit_error(
                f"""Wrong number of arguments while executing {prg_cntr+1}. command""",
                ErrorCode.XML_STRUCTURE_ERROR)

    op1 = CoreData.stack_pop()

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

    CoreData.stack_push(not op1.value)
    return prg_cntr + 1

def int2chars(prg_cntr: int, args: list):
    """ Convert number <symb> to ascii value character
        INT2CHARS
    """
    if len(args) != 0:
        ErrorCode.exit_error(
                f"""Wrong number of arguments while executing {prg_cntr+1}. command""",
                ErrorCode.XML_STRUCTURE_ERROR)

    op1 = CoreData.stack_pop()

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

    CoreData.stack_push(chr(op1.value))
    return prg_cntr + 1

def stri2ints(prg_cntr: int, args: list):
    """ Store ascii value of character at position <symb2> in string <symb1>
            in <var>
        STRI2INTS
    """
    if len(args) != 0:
        ErrorCode.exit_error(
                f"""Wrong number of arguments while executing {prg_cntr+1}. command""",
                ErrorCode.XML_STRUCTURE_ERROR)

    op2 = CoreData.stack_pop()
    op1 = CoreData.stack_pop()

    # initialization check
    if op1.type == 'UNDEF':
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

    CoreData.stack_push(ord(op1.value[op2.value]))
    return prg_cntr + 1

def int2floats(prg_cntr: int, args: list):
    """ Converts int value <symb> to float and store in <var>
        INT2FLOATS
    """
    if len(args) != 0:
        ErrorCode.exit_error(
                f"""Wrong number of arguments while executing {prg_cntr+1}. command""",
                ErrorCode.XML_STRUCTURE_ERROR)

    op1 = CoreData.stack_pop()

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

    CoreData.stack_push(float(op1.value))
    return prg_cntr + 1

def float2ints(prg_cntr: int, args: list):
    """ Converts float value <symb> to int and store in <var>
        FLOAT2INTS
    """
    if len(args) != 0:
        ErrorCode.exit_error(
                f"""Wrong number of arguments while executing {prg_cntr+1}. command""",
                ErrorCode.XML_STRUCTURE_ERROR)

    op1 = CoreData.stack_pop()

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

    CoreData.stack_push(int(op1.value))
    return prg_cntr + 1

def jumpifeqs(prg_cntr: int, args: list):
    """ Jump to <label> if <symb1> is equal to <symb2>
        JUMPIFEQS
    """
    if len(args) != 1:
        ErrorCode.exit_error(
                f"""Wrong number of arguments while executing {prg_cntr+1}. command""",
                ErrorCode.XML_STRUCTURE_ERROR)

    lbl_name = args[0].value
    op2 = CoreData.stack_pop()
    op1 = CoreData.stack_pop()

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

    return CoreData.labels[lbl_name] if op1.value == op2.value else prg_cntr + 1

def jumpifneqs(prg_cntr: int, args: list):
    """ Jump to <label> if <symb1> is not equal to <symb2>
        JUMPIFNEQS <label>
    """
    if len(args) != 1:
        ErrorCode.exit_error(
                f"""Wrong number of arguments while executing {prg_cntr+1}. command""",
                ErrorCode.XML_STRUCTURE_ERROR)

    lbl_name = args[0].value
    op2 = CoreData.stack_pop()
    op1 = CoreData.stack_pop()

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

    return CoreData.labels[lbl_name] if op1.value != op2.value else prg_cntr + 1
