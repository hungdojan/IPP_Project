import sys
from .error import ErrorCode
from .frame import Frame, Variable

UNICODE_MAX_VAL = 1,114,111

class CoreData:
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


def move(ins_order: int, args: list):
    var: Variable = CoreData.get_variable(args[0].value)
    op1 = CoreData.get_symbol(args[1])

    # initialization check
    if op1.type == 'UNDEF':
        sys.exit(ErrorCode.RUNTIME_MISSING_VALUE)

    var.value = op1.value
    return ins_order + 1


def createframe(ins_order: int, _):
    """ Creates temporary frame """
    CoreData.temp_frame = Frame()
    return ins_order + 1


def pushframe(ins_order: int, _):
    """ Push temporary frame to stack of frames """
    if CoreData.temp_frame is None or not CoreData.temp_frame.is_active:
        sys.exit(ErrorCode.RUNTIME_NONEXIST_FRAME)

    CoreData.stack_frames.append(CoreData.temp_frame)
    CoreData.temp_frame.is_active = False
    CoreData.local_frame = CoreData.temp_frame
    return ins_order + 1

def popframe(ins_order: int, _):
    """ Pop frame from stack of frames to temporary frame """
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
    """ Define new variable """
    var_name = args[0].value
    CoreData.add_variable(var_name)
    return ins_order + 1

def call(ins_order: int, args: list):
    """ Jump to label while perserving instruction pointer value """
    lbl_name = args[0].value
    if CoreData.labels.get(lbl_name) is None:
        sys.exit(ErrorCode.SEMANTIC_ERROR)

    CoreData.stack_func.append(ins_order)
    return CoreData.labels[lbl_name] - 1

def return_i(ins_order: int, _):
    """ Jump back to stored instruction pointer value """
    if len(CoreData.stack_func) == 0:
        sys.exit(ErrorCode.RUNTIME_MISSING_VALUE)

    ins_order = CoreData.stack_func.pop()
    return ins_order + 1

def pushs(ins_order: int, args: list):
    """ Push value to stack """
    if args[0].type == 'var':
        var = CoreData.get_variable(args[0].value)
        if var.type == 'UNDEF':
            sys.exit(ErrorCode.RUNTIME_MISSING_VALUE)
        value = var.value
    else:
        value = args[0].value

    # TODO: uninitialized variable
    CoreData.stack_vals.append(value)
    return ins_order + 1

def pops(ins_order: int, args: list):
    """ Pop data from stack to variable """
    var: Variable = CoreData.get_variable(args[0].value)

    # semantic checks
    if len(CoreData.stack_vals) == 0:
        sys.exit(ErrorCode.RUNTIME_MISSING_VALUE)

    stack_value = CoreData.stack_vals.pop()
    var.value = stack_value
    return ins_order + 1

def add(ins_order: int, args: list):
    var: Variable = CoreData.get_variable(args[0].value)
    op1 = CoreData.get_symbol(args[1])
    op2 = CoreData.get_symbol(args[2])

    # runtime type check
    if (op1.type not in ('int', 'float') or op2.type != ('int', 'float')
        or op1.type != op2.type):
        sys.exit(ErrorCode.RUNTIME_WRONG_TYPE)

    var.value = op1.value + op2.value

    return ins_order + 1

def sub(ins_order: int, args: list):
    var: Variable = CoreData.get_variable(args[0].value)
    op1 = CoreData.get_symbol(args[1])
    op2 = CoreData.get_symbol(args[2])

    # runtime type check
    if (op1.type not in ('int', 'float') or op2.type != ('int', 'float')
        or op1.type != op2.type):
        sys.exit(ErrorCode.RUNTIME_WRONG_TYPE)

    var.value = op1.value - op2.value
    return ins_order + 1

def mul(ins_order: int, args: list):
    var: Variable = CoreData.get_variable(args[0].value)
    op1 = CoreData.get_symbol(args[1])
    op2 = CoreData.get_symbol(args[2])

    # runtime type check
    if (op1.type not in ('int', 'float') or op2.type != ('int', 'float')
        or op1.type != op2.type):
        sys.exit(ErrorCode.RUNTIME_WRONG_TYPE)

    var.value = op1.value * op2.value
    return ins_order + 1

def div(ins_order: int, args: list):
    var: Variable = CoreData.get_variable(args[0].value)
    op1 = CoreData.get_symbol(args[1])
    op2 = CoreData.get_symbol(args[2])

    # runtime type check
    if (op1.type not in ('int', 'float') or op2.type != ('int', 'float')
        or op1.type != op2.type):
        sys.exit(ErrorCode.RUNTIME_WRONG_TYPE)

    var.value = op1.value / op2.value
    return ins_order + 1

def idiv(ins_order: int, args: list):
    var: Variable = CoreData.get_variable(args[0].value)
    op1 = CoreData.get_symbol(args[1])
    op2 = CoreData.get_symbol(args[2])

    # runtime type check
    if (op1.type not in ('int', 'float') or op2.type != ('int', 'float')
        or op1.type != op2.type):
        sys.exit(ErrorCode.RUNTIME_WRONG_TYPE)

    var.value = op1.value // op2.value
    return ins_order + 1

def lt(ins_order: int, args: list):
    var: Variable = CoreData.get_variable(args[0].value)
    op1 = CoreData.get_symbol(args[1])
    op2 = CoreData.get_symbol(args[2])

    # runtime type check
    if op1.type == 'nil' or op2.type == 'nil':
        sys.exit(ErrorCode.RUNTIME_WRONG_TYPE)
    if op1.type != op2.type:
        sys.exit(ErrorCode.RUNTIME_WRONG_TYPE)

    var.value = op1.value > op2.value
    return ins_order + 1

def gt(ins_order: int, args: list):
    var: Variable = CoreData.get_variable(args[0].value)
    op1 = CoreData.get_symbol(args[1])
    op2 = CoreData.get_symbol(args[2])

    # runtime type check
    if op1.type == 'nil' or op2.type == 'nil':
        sys.exit(ErrorCode.RUNTIME_WRONG_TYPE)
    if op1.type != op2.type:
        sys.exit(ErrorCode.RUNTIME_WRONG_TYPE)

    var.value = op1.value < op2.value
    return ins_order + 1

def eq(ins_order: int, args: list):
    var: Variable = CoreData.get_variable(args[0].value)
    op1 = CoreData.get_symbol(args[1])
    op2 = CoreData.get_symbol(args[2])

    # runtime type check
    if op1.type != op2.type and (op1.type != 'nil' or op2.type != 'nil'):
        sys.exit(ErrorCode.RUNTIME_WRONG_TYPE)

    var.value = op1.value == op2.value
    return ins_order + 1

def and_i(ins_order: int, args: list):
    var: Variable = CoreData.get_variable(args[0].value)
    op1 = CoreData.get_symbol(args[1])
    op2 = CoreData.get_symbol(args[2])

    # runtime type check
    if op1.type != 'bool' or op2.type != 'bool':
        sys.exit(ErrorCode.RUNTIME_WRONG_TYPE)

    var.value = op1.value and op2.value
    return ins_order + 1

def or_i(ins_order: int, args: list):
    var: Variable = CoreData.get_variable(args[0].value)
    op1 = CoreData.get_symbol(args[1])
    op2 = CoreData.get_symbol(args[2])

    # runtime type check
    if op1.type != 'bool' or op2.type != 'bool':
        sys.exit(ErrorCode.RUNTIME_WRONG_TYPE)

    var.value = op1.value or op2.value
    return ins_order + 1

def not_i(ins_order: int, args: list):
    var: Variable = CoreData.get_variable(args[0].value)
    op1 = CoreData.get_symbol(args[1])

    # runtime type check
    if op1.type != 'bool':
        sys.exit(ErrorCode.RUNTIME_WRONG_TYPE)

    var.value = not op1.value
    return ins_order + 1

def int2char(ins_order: int, args: list):
    var: Variable = CoreData.get_variable(args[0].value)
    op1 = CoreData.get_symbol(args[1])

    # runtime type check
    if op1.type != 'int':
        sys.exit(ErrorCode.RUNTIME_WRONG_TYPE)

    # ord function range check
    if op1.value not in range(UNICODE_MAX_VAL + 1):
        sys.exit(ErrorCode.RUNTIME_STRING_HANDLING)

    var.value = chr(op1.value)
    return ins_order + 1

def stri2int(ins_order: int, args: list):
    var: Variable = CoreData.get_variable(args[0].value)
    op1 = CoreData.get_symbol(args[1])
    op2 = CoreData.get_symbol(args[2])

    # runtime type check
    if op1.type != 'string' or op2.type != 'int':
        sys.exit(ErrorCode.RUNTIME_WRONG_TYPE)

    # index range check
    if op2.value not in range(len(op1.value)):
        sys.exit(ErrorCode.RUNTIME_STRING_HANDLING)

    var.value = ord()
    return ins_order + 1

def int2float(ins_order: int, args: list):
    var: Variable = CoreData.get_variable(args[0].value)
    op1 = CoreData.get_symbol(args[1])

    if op1.type != 'int':
        sys.exit(ErrorCode.RUNTIME_WRONG_TYPE)

    var.value = float(op1.value)
    return ins_order + 1

def float2int(ins_order: int, args: list):
    var: Variable = CoreData.get_variable(args[0].value)
    op1 = CoreData.get_symbol(args[1])

    if op1.type != 'float':
        sys.exit(ErrorCode.RUNTIME_WRONG_TYPE)

    var.value = int(op1.value)
    return ins_order + 1

def read(ins_order: int, args: list):
    var: Variable = CoreData.get_variable(args[0].value)

    # data type
    op1 = CoreData.get_symbol(args[1])

    if op1.value == 'string':
        var.value = input()
    elif op1.value == 'bool':
        var.value == (input() == 'true')
    elif op1.value == 'int':
        try:
            var.value = int(input())
        except:
            var.value = None
    elif op1.value == 'float':
        try:
            var.value = float(input())
        except:
            var.value = None
    else:
        sys.exit(ErrorCode.RUNTIME_WRONG_VALUE) # TODO: what??

    return ins_order + 1

def write(ins_order: int, args: list):
    symb = CoreData.get_symbol(args[0])

    if symb.type == 'nil':
        print('', end='', flush=True)
    elif symb.type == 'bool':
        output_msg = 'true' if symb.value else 'false'
        print(output_msg, end='', flush=True)
    else:
        print(symb.value, end='', flush=True)
    return ins_order + 1

def concat(ins_order: int, args: list):
    var: Variable = CoreData.get_variable(args[0].value)
    op1 = CoreData.get_symbol(args[1])
    op2 = CoreData.get_symbol(args[2])

    # runtime type check
    if op1.type != 'string' or op2.type != 'string':
        sys.exit(ErrorCode.RUNTIME_WRONG_TYPE)

    var.value = op1.value + op2.value
    return ins_order + 1

def strlen(ins_order: int, args: list):
    var: Variable = CoreData.get_variable(args[0].value)
    op1 = CoreData.get_symbol(args[1])

    # runtime type check
    if op1.type != 'string':
        sys.exit(ErrorCode.RUNTIME_WRONG_TYPE)

    var.value = len(op1.value)
    return ins_order + 1

def getchar(ins_order: int, args: list):
    var: Variable = CoreData.get_variable(args[0].value)
    op1 = CoreData.get_symbol(args[1])
    op2 = CoreData.get_symbol(args[2])

    # runtime type check
    if op1.type != 'string' or op2.type != 'int':
        sys.exit(ErrorCode.RUNTIME_WRONG_TYPE)

    # index range check
    if op2.value not in range(len(op1.value)):
        sys.exit(ErrorCode.RUNTIME_STRING_HANDLING)

    var.value = op1.value[op2.value]
    return ins_order + 1

def setchar(ins_order: int, args: list):
    var: Variable = CoreData.get_variable(args[0].value)
    op1 = CoreData.get_symbol(args[1])
    op2 = CoreData.get_symbol(args[2])

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
    var: Variable = CoreData.get_variable(args[0].value)
    op1 = CoreData.get_symbol(args[1])

    # runtime type check
    if op1.type == 'UNDEF':
        op1.value = ''

    var.value = op1.type
    return ins_order + 1

def label(ins_order: int, _):
    return ins_order + 1

def jump(ins_order: int, args: list):
    lbl_name = args[0].value

    # label check
    ins_order = CoreData.labels.get(lbl_name)
    if ins_order is None:
        sys.exit(ErrorCode.SEMANTIC_ERROR)

    return ins_order

def jumpifeq(ins_order: int, args: list):
    lbl_name = args[0].value
    op1 = CoreData.get_symbol(args[1])
    op2 = CoreData.get_symbol(args[2])

    # label check
    index_if_true = CoreData.labels.get(lbl_name)
    if index_if_true is None:
        sys.exit(ErrorCode.SEMANTIC_ERROR)

    # runtime type check
    if op1.type != op2.type and (op1.type != 'nil' or op2.type != 'nil'):
        sys.exit(ErrorCode.RUNTIME_WRONG_TYPE)

    return index_if_true if op1.value == op2.value else ins_order + 1

def jumpifneq(ins_order: int, args: list):
    lbl_name = args[0].value
    op1 = CoreData.get_symbol(args[1])
    op2 = CoreData.get_symbol(args[2])

    # label check
    index_if_true = CoreData.labels.get(lbl_name)
    if index_if_true is None:
        sys.exit(ErrorCode.SEMANTIC_ERROR)

    # runtime type check
    if op1.type != op2.type and (op1.type != 'nil' or op2.type != 'nil'):
        sys.exit(ErrorCode.RUNTIME_WRONG_TYPE)

    return index_if_true if op1.value != op2.value else ins_order + 1

def exit_i(ins_order: int, args: list):
    symb  = CoreData.get_symbol(args[0])

    # initialization check
    if symb.type != 'int':
        sys.exit(ErrorCode.RUNTIME_WRONG_TYPE)

    if symb.value not in range(50):
        sys.exit(ErrorCode.RUNTIME_WRONG_VALUE)
    # dead code
    return ins_order + 1

def dprint(ins_order: int, args: list):
    symb = CoreData.get_symbol(args[0])

    # initialization check
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

def break_i(ins_order: int, args: list):
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
