import re
import sys
from .error import ErrorCode
from .coredata import CoreData
from .frame import Frame, Variable

UNICODE_MAX_VAL: int = 1_114_111

def move(ins_order: int, args: list):
    """ Move value <symb> to <var>
        MOVE <var> <symb>
    """
    if len(args) != 2:
        sys.exit(ErrorCode.XML_STRUCTURE_ERROR)

    var: Variable = CoreData.get_variable(args[0].value)
    op1 = CoreData.get_symbol(args[1])

    # initialization check
    if op1.type == 'UNDEF':
        sys.exit(ErrorCode.RUNTIME_MISSING_VALUE)

    var.value = op1.value
    return ins_order + 1


def createframe(ins_order: int, args: list):
    """ Creates temporary frame """
    if len(args) != 0:
        sys.exit(ErrorCode.XML_STRUCTURE_ERROR)

    CoreData.temp_frame = Frame()
    return ins_order + 1


def pushframe(ins_order: int, args: list):
    """ Push temporary frame to stack of frames """
    if len(args) != 0:
        sys.exit(ErrorCode.XML_STRUCTURE_ERROR)

    if CoreData.temp_frame is None or not CoreData.temp_frame.is_active:
        sys.exit(ErrorCode.RUNTIME_NONEXIST_FRAME)

    CoreData.stack_frames.append(CoreData.temp_frame)
    CoreData.temp_frame.is_active = False
    CoreData.local_frame = CoreData.temp_frame
    return ins_order + 1

def popframe(ins_order: int, args: list):
    """ Pop frame from stack of frames to temporary frame """
    if len(args) != 0:
        sys.exit(ErrorCode.XML_STRUCTURE_ERROR)

    if len(CoreData.stack_frames) == 0:
        sys.exit(ErrorCode.RUNTIME_NONEXIST_FRAME)

    CoreData.temp_frame = CoreData.stack_frames.pop()
    CoreData.temp_frame.is_active = True
    # set local frame
    if len(CoreData.stack_frames) == 0:
        CoreData.local_frame = None
    else:
        CoreData.local_frame = CoreData.stack_frames[-1]
    return ins_order + 1

def defvar(ins_order: int, args: list):
    """ Define new <var>
        DEFVAR <var>
    """
    if len(args) != 1:
        sys.exit(ErrorCode.XML_STRUCTURE_ERROR)

    var_name = args[0].value
    CoreData.add_variable(var_name)
    return ins_order + 1

def call(ins_order: int, args: list):
    """ Jump to <label> while perserving instruction pointer value
        CALL <label>
    """
    if len(args) != 1:
        sys.exit(ErrorCode.XML_STRUCTURE_ERROR)

    lbl_name = args[0].value
    if CoreData.labels.get(lbl_name) is None:
        sys.exit(ErrorCode.SEMANTIC_ERROR)

    CoreData.stack_func.append(ins_order)
    return CoreData.labels[lbl_name] - 1

def return_i(ins_order: int, args: list):
    """ Jump back to stored instruction pointer value """
    if len(args) != 0:
        sys.exit(ErrorCode.XML_STRUCTURE_ERROR)

    if len(CoreData.stack_func) == 0:
        sys.exit(ErrorCode.RUNTIME_MISSING_VALUE)

    ins_order = CoreData.stack_func.pop()
    return ins_order + 1

def pushs(ins_order: int, args: list):
    """ Push value of <symb> to stack
        PUSHS <symb>
    """
    if len(args) != 1:
        sys.exit(ErrorCode.XML_STRUCTURE_ERROR)

    if args[0].type == 'var':
        var = CoreData.get_variable(args[0].value)
        if var.type == 'UNDEF':
            sys.exit(ErrorCode.RUNTIME_MISSING_VALUE)
        value = var.value
    else:
        value = args[0].value

    CoreData.stack_vals.append(value)
    return ins_order + 1

def pops(ins_order: int, args: list):
    """ Pop data from stack to <var>
        POPS <var>
    """
    if len(args) != 1:
        sys.exit(ErrorCode.XML_STRUCTURE_ERROR)

    var: Variable = CoreData.get_variable(args[0].value)

    # semantic checks
    if len(CoreData.stack_vals) == 0:
        sys.exit(ErrorCode.RUNTIME_MISSING_VALUE)

    stack_value = CoreData.stack_vals.pop()
    var.value = stack_value
    return ins_order + 1

def add(ins_order: int, args: list):
    """ Add two numbers and store in <var>
        ADD <var> <symb> <symb>
    """
    if len(args) != 3:
        sys.exit(ErrorCode.XML_STRUCTURE_ERROR)

    var: Variable = CoreData.get_variable(args[0].value)
    op1 = CoreData.get_symbol(args[1])
    op2 = CoreData.get_symbol(args[2])

    # initialization check
    if op1.type == 'UNDEF' or op2.type == 'UNDEF':
        sys.exit(ErrorCode.RUNTIME_MISSING_VALUE)
    # runtime type check
    if (op1.type not in ('int', 'float') or op2.type not in ('int', 'float')
        or op1.type != op2.type):
        sys.exit(ErrorCode.RUNTIME_WRONG_TYPE)

    var.value = op1.value + op2.value

    return ins_order + 1

def sub(ins_order: int, args: list):
    """ Subtract two numbers and store in <var>
        SUB <var> <symb> <symb>
    """
    if len(args) != 3:
        sys.exit(ErrorCode.XML_STRUCTURE_ERROR)

    var: Variable = CoreData.get_variable(args[0].value)
    op1 = CoreData.get_symbol(args[1])
    op2 = CoreData.get_symbol(args[2])

    # initialization check
    if op1.type == 'UNDEF' or op2.type == 'UNDEF':
        sys.exit(ErrorCode.RUNTIME_MISSING_VALUE)
    # runtime type check
    if (op1.type not in ('int', 'float') or op2.type not in ('int', 'float')
        or op1.type != op2.type):
        sys.exit(ErrorCode.RUNTIME_WRONG_TYPE)

    var.value = op1.value - op2.value
    return ins_order + 1

def mul(ins_order: int, args: list):
    """ Multiply two numbers and store in <var>
        MUL <var> <symb> <symb>
    """
    if len(args) != 3:
        sys.exit(ErrorCode.XML_STRUCTURE_ERROR)

    var: Variable = CoreData.get_variable(args[0].value)
    op1 = CoreData.get_symbol(args[1])
    op2 = CoreData.get_symbol(args[2])

    # initialization check
    if op1.type == 'UNDEF' or op2.type == 'UNDEF':
        sys.exit(ErrorCode.RUNTIME_MISSING_VALUE)
    # runtime type check
    if (op1.type not in ('int', 'float') or op2.type not in ('int', 'float')
        or op1.type != op2.type):
        sys.exit(ErrorCode.RUNTIME_WRONG_TYPE)

    var.value = op1.value * op2.value
    return ins_order + 1

def div(ins_order: int, args: list):
    """ Divide two numbers and store in <var>
        DIV <var> <symb> <symb>
    """
    if len(args) != 3:
        sys.exit(ErrorCode.XML_STRUCTURE_ERROR)

    var: Variable = CoreData.get_variable(args[0].value)
    op1 = CoreData.get_symbol(args[1])
    op2 = CoreData.get_symbol(args[2])

    # initialization check
    if op1.type == 'UNDEF' or op2.type == 'UNDEF':
        sys.exit(ErrorCode.RUNTIME_MISSING_VALUE)
    # runtime type check
    if (op1.type not in ('int', 'float') or op2.type not in ('int', 'float')
        or op1.type != op2.type):
        sys.exit(ErrorCode.RUNTIME_WRONG_TYPE)

    # div zero check
    if op2.value == 0:
        sys.exit(ErrorCode.RUNTIME_WRONG_VALUE)

    var.value = op1.value / op2.value
    return ins_order + 1

def idiv(ins_order: int, args: list):
    """ Divide two numbers and store in <var> round down value
        IDIV <var> <symb> <symb>
    """
    if len(args) != 3:
        sys.exit(ErrorCode.XML_STRUCTURE_ERROR)

    var: Variable = CoreData.get_variable(args[0].value)
    op1 = CoreData.get_symbol(args[1])
    op2 = CoreData.get_symbol(args[2])

    # initialization check
    if op1.type == 'UNDEF' or op2.type == 'UNDEF':
        sys.exit(ErrorCode.RUNTIME_MISSING_VALUE)
    # runtime type check
    if (op1.type not in ('int', 'float') or op2.type not in ('int', 'float')
        or op1.type != op2.type):
        sys.exit(ErrorCode.RUNTIME_WRONG_TYPE)

    # div zero check
    if op2.value == 0:
        sys.exit(ErrorCode.RUNTIME_WRONG_VALUE)

    var.value = op1.value // op2.value
    return ins_order + 1

def lt(ins_order: int, args: list):
    """ Check if <symb1> is less than <symb2>; store in <var>
        LT <var> <symb1> <symb2>
    """
    if len(args) != 3:
        sys.exit(ErrorCode.XML_STRUCTURE_ERROR)

    var: Variable = CoreData.get_variable(args[0].value)
    op1 = CoreData.get_symbol(args[1])
    op2 = CoreData.get_symbol(args[2])

    # initialization check
    if op1.type == 'UNDEF' or op2.type == 'UNDEF':
        sys.exit(ErrorCode.RUNTIME_MISSING_VALUE)
    # runtime type check
    if op1.type == 'nil' or op2.type == 'nil':
        sys.exit(ErrorCode.RUNTIME_WRONG_TYPE)
    if op1.type != op2.type:
        sys.exit(ErrorCode.RUNTIME_WRONG_TYPE)

    var.value = op1.value > op2.value
    return ins_order + 1

def gt(ins_order: int, args: list):
    """ Check if <symb1> is greater than <symb2>; store in <var>
        GT <var> <symb1> <symb2>
    """
    if len(args) != 3:
        sys.exit(ErrorCode.XML_STRUCTURE_ERROR)

    var: Variable = CoreData.get_variable(args[0].value)
    op1 = CoreData.get_symbol(args[1])
    op2 = CoreData.get_symbol(args[2])

    # initialization check
    if op1.type == 'UNDEF' or op2.type == 'UNDEF':
        sys.exit(ErrorCode.RUNTIME_MISSING_VALUE)
    # runtime type check
    if op1.type == 'nil' or op2.type == 'nil':
        sys.exit(ErrorCode.RUNTIME_WRONG_TYPE)
    if op1.type != op2.type:
        sys.exit(ErrorCode.RUNTIME_WRONG_TYPE)

    var.value = op1.value < op2.value
    return ins_order + 1

def eq(ins_order: int, args: list):
    """ Check if <symb1> and <symb2> values are equal; store in <var>
        EQ <var> <symb1> <symb2>
    """
    if len(args) != 3:
        sys.exit(ErrorCode.XML_STRUCTURE_ERROR)

    var: Variable = CoreData.get_variable(args[0].value)
    op1 = CoreData.get_symbol(args[1])
    op2 = CoreData.get_symbol(args[2])

    # initialization check
    if op1.type == 'UNDEF' or op2.type == 'UNDEF':
        sys.exit(ErrorCode.RUNTIME_MISSING_VALUE)
    # runtime type check
    if op1.type != op2.type and (op1.type != 'nil' or op2.type != 'nil'):
        sys.exit(ErrorCode.RUNTIME_WRONG_TYPE)

    var.value = op1.value == op2.value
    return ins_order + 1

def and_i(ins_order: int, args: list):
    """ Store 'true' in <var> if both <symb1> and <symb2> are 'true'
            otherwise store 'false'
        AND <var> <symb1> <symb2>
    """
    if len(args) != 3:
        sys.exit(ErrorCode.XML_STRUCTURE_ERROR)

    var: Variable = CoreData.get_variable(args[0].value)
    op1 = CoreData.get_symbol(args[1])
    op2 = CoreData.get_symbol(args[2])

    # initialization check
    if op1.type == 'UNDEF' or op2.type == 'UNDEF':
        sys.exit(ErrorCode.RUNTIME_MISSING_VALUE)
    # runtime type check
    if op1.type != 'bool' or op2.type != 'bool':
        sys.exit(ErrorCode.RUNTIME_WRONG_TYPE)

    var.value = op1.value and op2.value
    return ins_order + 1

def or_i(ins_order: int, args: list):
    """ Store 'false' in <var> if both <symb1> and <symb2> are 'false'
            otherwise store 'true'
        OR <var> <symb1> <symb2>
    """
    if len(args) != 3:
        sys.exit(ErrorCode.XML_STRUCTURE_ERROR)

    var: Variable = CoreData.get_variable(args[0].value)
    op1 = CoreData.get_symbol(args[1])
    op2 = CoreData.get_symbol(args[2])

    # initialization check
    if op1.type == 'UNDEF' or op2.type == 'UNDEF':
        sys.exit(ErrorCode.RUNTIME_MISSING_VALUE)
    # runtime type check
    if op1.type != 'bool' or op2.type != 'bool':
        sys.exit(ErrorCode.RUNTIME_WRONG_TYPE)

    var.value = op1.value or op2.value
    return ins_order + 1

def not_i(ins_order: int, args: list):
    """ Negate <symb> value and store in <var>
        NOT <var> <symb>
    """
    if len(args) != 2:
        sys.exit(ErrorCode.XML_STRUCTURE_ERROR)

    var: Variable = CoreData.get_variable(args[0].value)
    op1 = CoreData.get_symbol(args[1])

    # initialization check
    if op1.type == 'UNDEF':
        sys.exit(ErrorCode.RUNTIME_MISSING_VALUE)
    # runtime type check
    if op1.type != 'bool':
        sys.exit(ErrorCode.RUNTIME_WRONG_TYPE)

    var.value = not op1.value
    return ins_order + 1

def int2char(ins_order: int, args: list):
    """ Convert number <symb> to ascii value character
        INT2CHAR <var> <symb>
    """
    if len(args) != 2:
        sys.exit(ErrorCode.XML_STRUCTURE_ERROR)

    var: Variable = CoreData.get_variable(args[0].value)
    op1 = CoreData.get_symbol(args[1])

    # initialization check
    if op1.type == 'UNDEF':
        sys.exit(ErrorCode.RUNTIME_MISSING_VALUE)
    # runtime type check
    if op1.type != 'int':
        sys.exit(ErrorCode.RUNTIME_WRONG_TYPE)

    # ord function range check
    if op1.value not in range(UNICODE_MAX_VAL + 1):
        sys.exit(ErrorCode.RUNTIME_STRING_HANDLING)

    var.value = chr(op1.value)
    return ins_order + 1

def stri2int(ins_order: int, args: list):
    """ Store ascii value of character at position <symb2> in string <symb1>
            in <var>
        STRI2INT <var> <symb1> <symb2>
    """
    if len(args) != 3:
        sys.exit(ErrorCode.XML_STRUCTURE_ERROR)

    var: Variable = CoreData.get_variable(args[0].value)
    op1 = CoreData.get_symbol(args[1])
    op2 = CoreData.get_symbol(args[2])

    # initialization check
    if op1.type == 'UNDEF':
        sys.exit(ErrorCode.RUNTIME_MISSING_VALUE)
    # runtime type check
    if op1.type != 'string' or op2.type != 'int':
        sys.exit(ErrorCode.RUNTIME_WRONG_TYPE)

    # index range check
    if op2.value not in range(len(op1.value)):
        sys.exit(ErrorCode.RUNTIME_STRING_HANDLING)

    var.value = ord()
    return ins_order + 1

def int2float(ins_order: int, args: list):
    """ Converts int value <symb> to float and store in <var>
        INT2FLOAT <var> <symb>
    """
    if len(args) != 2:
        sys.exit(ErrorCode.XML_STRUCTURE_ERROR)

    var: Variable = CoreData.get_variable(args[0].value)
    op1 = CoreData.get_symbol(args[1])

    # initialization check
    if op1.type == 'UNDEF':
        sys.exit(ErrorCode.RUNTIME_MISSING_VALUE)
    # runtime type check
    if op1.type != 'int':
        sys.exit(ErrorCode.RUNTIME_WRONG_TYPE)

    var.value = float(op1.value)
    return ins_order + 1

def float2int(ins_order: int, args: list):
    """ Converts float value <symb> to int and store in <var>
        FLOAT2INT <var> <symb>
    """
    if len(args) != 2:
        sys.exit(ErrorCode.XML_STRUCTURE_ERROR)

    var: Variable = CoreData.get_variable(args[0].value)
    op1 = CoreData.get_symbol(args[1])

    # initialization check
    if op1.type == 'UNDEF':
        sys.exit(ErrorCode.RUNTIME_MISSING_VALUE)
    # runtime type check
    if op1.type != 'float':
        sys.exit(ErrorCode.RUNTIME_WRONG_TYPE)

    var.value = int(op1.value)
    return ins_order + 1

def read(ins_order: int, args: list):
    """ Read from input file <type> and store in <var>
        READ <var> <type>
    """
    if len(args) != 2:
        sys.exit(ErrorCode.XML_STRUCTURE_ERROR)

    var: Variable = CoreData.get_variable(args[0].value)

    # data type
    op1 = CoreData.get_symbol(args[1])
    input_value = CoreData.get_line()

    if op1.value == 'string':
        var.value = input_value
    elif op1.value == 'bool':
        var.value = (input_value == 'true')
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
        sys.exit(ErrorCode.RUNTIME_WRONG_VALUE)

    return ins_order + 1

def write(ins_order: int, args: list):
    """ Write to STDIN <symb> value
        WRITE <symb>
    """
    if len(args) != 1:
        sys.exit(ErrorCode.XML_STRUCTURE_ERROR)

    symb = CoreData.get_symbol(args[0])

    if symb.type == 'UNDEF':
        sys.exit(ErrorCode.RUNTIME_MISSING_VALUE)

    if symb.type == 'nil':
        print('', end='', flush=True)
    elif symb.type == 'bool':
        output_msg = 'true' if symb.value else 'false'
        print(output_msg, end='', flush=True)
    elif symb.type == 'float':
        print(float.hex(symb.value), end='', flush=True)
    else:
        print(symb.value, end='', flush=True)
    return ins_order + 1

def concat(ins_order: int, args: list):
    """ Concatenate <symb2> to <symb1>; store in <var>
        CONCAR <var> <symb1> <symb2>
    """
    if len(args) != 3:
        sys.exit(ErrorCode.XML_STRUCTURE_ERROR)

    var: Variable = CoreData.get_variable(args[0].value)
    op1 = CoreData.get_symbol(args[1])
    op2 = CoreData.get_symbol(args[2])

    # initialization check
    if op1.type == 'UNDEF' or op2.type == 'UNDEF':
        sys.exit(ErrorCode.RUNTIME_MISSING_VALUE)
    # runtime type check
    if op1.type != 'string' or op2.type != 'string':
        sys.exit(ErrorCode.RUNTIME_WRONG_TYPE)

    var.value = op1.value + op2.value
    return ins_order + 1

def strlen(ins_order: int, args: list):
    """ Store string length of <symb> in <var>
        STRLEN <var> <symb>
    """
    if len(args) != 2:
        sys.exit(ErrorCode.XML_STRUCTURE_ERROR)

    var: Variable = CoreData.get_variable(args[0].value)
    op1 = CoreData.get_symbol(args[1])

    # initialization check
    if op1.type == 'UNDEF':
        sys.exit(ErrorCode.RUNTIME_MISSING_VALUE)
    # runtime type check
    if op1.type != 'string':
        sys.exit(ErrorCode.RUNTIME_WRONG_TYPE)

    var.value = len(op1.value)
    return ins_order + 1

def getchar(ins_order: int, args: list):
    """ Get character of <symb1> at position <symb2>; store in <var>
        GETCHAR <var> <symb1> <symb2>
    """
    if len(args) != 3:
        sys.exit(ErrorCode.XML_STRUCTURE_ERROR)

    var: Variable = CoreData.get_variable(args[0].value)
    op1 = CoreData.get_symbol(args[1])
    op2 = CoreData.get_symbol(args[2])

    # initialization check
    if op1.type == 'UNDEF' or op2.type == 'UNDEF':
        sys.exit(ErrorCode.RUNTIME_MISSING_VALUE)
    # runtime type check
    if op1.type != 'string' or op2.type != 'int':
        sys.exit(ErrorCode.RUNTIME_WRONG_TYPE)

    # index range check
    if op2.value not in range(len(op1.value)):
        sys.exit(ErrorCode.RUNTIME_STRING_HANDLING)

    var.value = op1.value[op2.value]
    return ins_order + 1

def setchar(ins_order: int, args: list):
    """ Set character of <symb1> at position <symb2>; store in <var>
        SETCHAR <var> <symb1> <symb2>
    """
    if len(args) != 3:
        sys.exit(ErrorCode.XML_STRUCTURE_ERROR)

    var: Variable = CoreData.get_variable(args[0].value)
    op1 = CoreData.get_symbol(args[1])
    op2 = CoreData.get_symbol(args[2])

    # initialization check
    if op1.type == 'UNDEF' or op2.type == 'UNDEF':
        sys.exit(ErrorCode.RUNTIME_MISSING_VALUE)
    # runtime type check
    if var.type != 'string' or op1.type != 'int' or op2.type != 'string':
        sys.exit(ErrorCode.RUNTIME_WRONG_TYPE)

    # index range check
    if op1.value not in range(len(var.value)) or len(op2.value) == 0:
        sys.exit(ErrorCode.RUNTIME_STRING_HANDLING)

    # ----- setchar ------
    new_char = op2.value[0]
    new_str  = list(var.value)
    new_str[op1.value] = new_char
    var.value = ''.join(new_str)
    # --------------------
    return ins_order + 1

def type_i(ins_order: int, args: list):
    """ Store type of <symb> in string form in <var>
        TYPE <var> <symb>
    """
    if len(args) != 2:
        sys.exit(ErrorCode.XML_STRUCTURE_ERROR)

    var: Variable = CoreData.get_variable(args[0].value)
    op1 = CoreData.get_symbol(args[1])

    # runtime type check
    if op1.type == 'UNDEF':
        var.value = ''
    else:
        var.value = op1.type
    return ins_order + 1

def label(ins_order: int, args: list):
    """ Label to jump
        LABEL <label>
    """
    if len(args) != 1:
        sys.exit(ErrorCode.XML_STRUCTURE_ERROR)

    return ins_order + 1

def jump(ins_order: int, args: list):
    """ Jump to <label>
        JUMP <label>
    """
    if len(args) != 1:
        sys.exit(ErrorCode.XML_STRUCTURE_ERROR)

    lbl_name = args[0].value

    # label check
    ins_order = CoreData.labels.get(lbl_name)
    if ins_order is None:
        sys.exit(ErrorCode.SEMANTIC_ERROR)

    return ins_order

def jumpifeq(ins_order: int, args: list):
    """ Jump to <label> if <symb1> is equal to <symb2>
        JUMPIFEQ <label> <symb1> <sym2>
    """
    if len(args) != 3:
        sys.exit(ErrorCode.XML_STRUCTURE_ERROR)

    lbl_name = args[0].value
    op1 = CoreData.get_symbol(args[1])
    op2 = CoreData.get_symbol(args[2])

    # initialization check
    if op1.type == 'UNDEF' or op2.type == 'UNDEF':
        sys.exit(ErrorCode.RUNTIME_MISSING_VALUE)
    # label check
    index_if_true = CoreData.labels.get(lbl_name)
    if index_if_true is None:
        sys.exit(ErrorCode.SEMANTIC_ERROR)

    # runtime type check
    if op1.type != op2.type and (op1.type != 'nil' or op2.type != 'nil'):
        sys.exit(ErrorCode.RUNTIME_WRONG_TYPE)

    return index_if_true if op1.value == op2.value else ins_order + 1

def jumpifneq(ins_order: int, args: list):
    """ Jump to <label> if <symb1> is not equal to <symb2>
        JUMPIFNEQ <label> <symb1> <sym2>
    """
    if len(args) != 3:
        sys.exit(ErrorCode.XML_STRUCTURE_ERROR)

    lbl_name = args[0].value
    op1 = CoreData.get_symbol(args[1])
    op2 = CoreData.get_symbol(args[2])

    # initialization check
    if op1.type == 'UNDEF' or op2.type == 'UNDEF':
        sys.exit(ErrorCode.RUNTIME_MISSING_VALUE)
    # label check
    index_if_true = CoreData.labels.get(lbl_name)
    if index_if_true is None:
        sys.exit(ErrorCode.SEMANTIC_ERROR)

    # runtime type check
    if op1.type != op2.type and (op1.type != 'nil' or op2.type != 'nil'):
        sys.exit(ErrorCode.RUNTIME_WRONG_TYPE)

    return index_if_true if op1.value != op2.value else ins_order + 1

def exit_i(ins_order: int, args: list):
    """ Exit program with <symb> value
        EXIT <symb>
    """
    if len(args) != 1:
        sys.exit(ErrorCode.XML_STRUCTURE_ERROR)

    symb  = CoreData.get_symbol(args[0])

    # runtime type check
    if symb.type != 'int':
        sys.exit(ErrorCode.RUNTIME_WRONG_TYPE)

    # value range check
    if symb.value not in range(50):
        sys.exit(ErrorCode.RUNTIME_WRONG_VALUE)

    # dead code
    sys.exit(symb.value)
    return ins_order + 1

def dprint(ins_order: int, args: list):
    """ Write <symb> value to STDERR
        DPRINT <symb>
    """
    if len(args) != 1:
        sys.exit(ErrorCode.XML_STRUCTURE_ERROR)

    symb = CoreData.get_symbol(args[0])

    # runtime type check
    if symb.type == 'UNDEF':
        sys.exit(ErrorCode.RUNTIME_MISSING_VALUE)

    if symb.type == 'nil':
        sys.stderr.write('')
    elif symb.type == 'bool':
        output_msg = 'true' if symb.value else 'false'
        sys.stderr.write(output_msg)
    else:
        sys.stderr.write(symb.value)
    return ins_order + 1

def break_i(ins_order: int, _):
    """ Write program debug information to STDERR
        BREAK
    """
    if len(args) != 0:
        sys.exit(ErrorCode.XML_STRUCTURE_ERROR)

    sys.stderr.write("================================\n")
    sys.stderr.write(f"Pozice v kodu: {ins_order + 1}. \n")

    # item[0] -> var name
    # item[1] -> var value
    sys.stderr.write("\nObsah globalniho ramce: \n")
    for item in CoreData.global_frame.vars.items():
        sys.stderr.write(f"\t{item[0]}: {item[1]}\n")

    sys.stderr.write("\nObsah lokalniho ramce: \n")
    for item in CoreData.local_frame.vars.items():
        sys.stderr.write(f"\t{item[0]}: {item[1]}\n")

    sys.stderr.write("\nObsah docasneho ramce: \n")
    for item in CoreData.temp_frame.vars.items():
        sys.stderr.write(f"\t{item[0]}: {item[1]}\n")

    sys.stderr.write(f"Pocet vykonanych instrukci: {CoreData.ins_performed}\n")
    sys.stderr.write("================================\n")

    return ins_order + 1

instruct_set = {
        'MOVE' : move,
        'CREATEFRAME' : createframe,
        'PUSHFRAME' : pushframe,
        'POPFRAME' : popframe,
        'DEFVAR' : defvar,
        'CALL' : call,
        'RETURN' : return_i,
        'PUSHS' : pushs,
        'POPS' : pops,
        'ADD' : add,
        'SUB' : sub,
        'MUL' : mul,
        'DIV' : div,
        'IDIV' : idiv,
        'LT' : lt,
        'GT' : gt,
        'EQ' : eq,
        'AND' : and_i,
        'OR' : or_i,
        'NOT' : not_i,
        'INT2CHAR' : int2char,
        'STRI2INT' : stri2int,
        'INT2FLOAT' : int2float,
        'FLOAT2INT' : float2int,
        'READ' : read,
        'WRITE' : write,
        'CONCAT' : concat,
        'STRLEN' : strlen,
        'GETCHAR' : getchar,
        'SETCHAR' : setchar,
        'TYPE' : type_i,
        'LABEL' : label,
        'JUMP' : jump,
        'JUMPIFEQ' : jumpifeq,
        'JUMPIFNEQ' : jumpifneq,
        'EXIT' : exit_i,
        'DPRINT' : dprint,
        'BREAK' : break_i
        }
