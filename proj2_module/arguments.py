import argparse
import sys
from .error import ErrorCode
from .coredata import CoreData

def arg_process():
    parser = argparse.ArgumentParser('IPPcode22 interpret')
    parser.add_argument('--source', action='store', metavar='filename',
            nargs=1, help='Zdrojovy soubor v XML formatu')
    parser.add_argument('--input', action='store', metavar='filename',
            nargs=1, help='Vstupni soubor')

    # TODO: stats

    args = parser.parse_args()
    if args.source is None and args.input is None:
        parser.error('Alespon jeden argument musi byt zavolan')
    if args.source:
        CoreData.source_file = args.source[0]
    if args.input:
        CoreData.input_file = open(args.input[0], 'r')
