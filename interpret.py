#!/usr/bin/env python3
from proj2_module.statement import Statement
from proj2_module.coredata import CoreData
from proj2_module.instruction_set import *
from proj2_module.arguments import arg_process
from proj2_module.xml_parser import xml_parser
from proj2_module.instruction_set import instruct_set



def main() -> int:
    # TODO: arguments
    arg_process()
    lof_ins = xml_parser()
    lof_ins.sort(key=(lambda statement: statement.order))
    CoreData.set_jumps(lof_ins)

    nof_ins = len(lof_ins)
    ins_index = 0
    while ins_index < nof_ins:
        stat: Statement = lof_ins[ins_index]
        ins_index = instruct_set[stat.ins](ins_index, stat.args)
        CoreData.ins_performed += 1


if __name__ == "__main__":
    exit(main());
