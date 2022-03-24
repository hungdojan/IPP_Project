"""File processes program's arguments

Author: Hung Do
File:   arguments.py
Module: proj2_module
"""
import argparse
from .coredata import CoreData

def arg_process():
    parser = argparse.ArgumentParser('IPPcode22 interpret')
    parser.add_argument('--source', action='store', metavar='filename',
            nargs=1, help='Zdrojovy soubor v XML formatu')
    parser.add_argument('--input', action='store', metavar='filename',
            nargs=1, help='Vstupni soubor')

    args = parser.parse_args()
    if args.source is None and args.input is None:
        parser.error('Alespon jeden argument musi byt zavolan')
    if args.source:
        CoreData.source_file = args.source[0]
    if args.input:
        # store file content as a list
        _f = open(args.input[0], 'r')
        CoreData.input_file = _f.read().split('\n')
        _f.close()
