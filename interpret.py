#!/usr/bin/env python3
import sys
import xml.etree.ElementTree as ET

from proj2_module.statement import Statement
from proj2_module.coredata import CoreData
from proj2_module.instruction_set import *
from proj2_module.arguments import arg_process

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

def xml_parser() -> list:
    lof_ins = []
    # TODO: check if file exists
    xml_path = sys.stdin if CoreData.source_file is None else CoreData.source_file
    tree = ET.parse(xml_path)
    program = tree.getroot()

    # loading operations
    for inst in program:
        opcode = inst.get('opcode').upper()
        order  = int(inst.get('order'))
        args   = []

        for i in range(3):
            arg = inst.find(f"arg{i+1}")
            if arg is None:
                break
            args.append((arg.get('type'), arg.text))
        lof_ins.append(Statement(opcode, order, args))

    if len(CoreData.undef_labels) > 0:
        # TODO: write output to stderr
        sys.exit(ErrorCode.SEMANTIC_ERROR)

    return lof_ins


def main() -> int:
    # TODO: arguments
    arg_process()
    lof_ins = xml_parser()
    lof_ins.sort(key=(lambda statement: statement.order))

    nof_ins = len(lof_ins)
    ins_index = 0
    while ins_index < nof_ins:
        stat: Statement = lof_ins[ins_index]
        ins_index = instruct_set[stat.ins](ins_index, stat.args)
        CoreData.ins_performed += 1


if __name__ == "__main__":
    exit(main());
