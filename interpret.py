#!/usr/bin/env python3
import sys
import xml.etree.ElementTree as ET

from proj2_module.statement import Statement
from proj2_module.coredata import CoreData, instruct_set

""" TODO:
    1. load arguments
    2. parse xml file
    3. sort it
    4. do command
        - semantic check
    5. exit code

    What do I need:
    lof_labels -> number of order
        -> for jumps

    scopes as class??
    global_scope |
    local_scope  |--> name, type and value it holds
    temp_scope   |

    lof_instructions -> function on it
        -> dictionary

    class for variable
        name
        type
        value

    file for constants???

    enum errors

    extended version:
    stack
    float
    stats
        -> class

"""

def xml_parser(xml_path: str) -> list:
    lof_ins = []
    # TODO: check if file exists
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

    return lof_ins


def main() -> int:
    # TODO: arguments
    lof_ins = xml_parser("./tmp.xml")
    lof_ins.sort(key=(lambda statement: statement.order))

    nof_ins = len(lof_ins)
    ins_index = 0
    while ins_index < nof_ins:
        stat: Statement = lof_ins[ins_index]
        ins_index = instruct_set[stat.ins](ins_index, stat.args)
        CoreData.ins_performed += 1

    # for ins in lof_ins:
    #     print(ins)
    # return 0

if __name__ == "__main__":
    exit(main());
