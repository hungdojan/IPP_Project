"""File processes program's arguments

Author: Hung Do
File:   arguments.py
Module: proj2_module
"""
import argparse
import os
from .coredata import CoreData
from .error import ErrorCode

def arg_process():
    parser = argparse.ArgumentParser('IPPcode22 interpreter')
    parser.add_argument('--source', action='store', metavar='filename',
            nargs=1, help='Source file in XML format')
    parser.add_argument('--input', action='store', metavar='filename',
            nargs=1, help='Input file')

    args = parser.parse_args()
    if args.source is None and args.input is None:
        parser.error('At least one argument must be used!')
    if args.source:
        if not os.path.exists(args.source[0]):
            ErrorCode.exit_error(f"File {args.source[0]} does not exists!",
                                 ErrorCode.UNDEFINED_ERROR)
        CoreData.source_file = args.source[0]
    if args.input:
        if not os.path.exists(args.input[0]):
            ErrorCode.exit_error(f"File {args.input[0]} does not exists!",
                                 ErrorCode.UNDEFINED_ERROR)
        # store file content as a list
        _f = open(args.input[0], 'r')
        CoreData.input_file = _f.read().split('\n')
        _f.close()
