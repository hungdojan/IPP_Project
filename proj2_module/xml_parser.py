"""Format checking for XML source code file.

Author: Hung Do
File:   xml_parser.py
Module: proj2_module
"""
import re
import sys
import xml.etree.ElementTree as ET

from xml.sax.handler import ContentHandler
from xml.sax import make_parser
from proj2_module.statement import Statement
from proj2_module.coredata import CoreData
from proj2_module.error import ErrorCode
from proj2_module.instruction_set import instruct_set

def format_validation(dtype: str, value):
    """XML data type value format validation

    Validation is done with regular expression stored in CoreData.REG_TYPE.

    Parameters:
    dtype (str): Symbol's data type 
    value (str): Symbol's value stored in string

    Returns:
    bool: True if value format is invalid otherwise False.

    """
    if dtype == 'var':
        if not re.match(f'^{CoreData.REG_TYPE["var"]}$', value):
            return True
    elif dtype == 'string':
        if not re.match(f'^{CoreData.REG_TYPE["string"]}$', value):
            return True
    elif dtype == 'type':
        if not re.match(f'^{CoreData.REG_TYPE["type"]}$', value):
            return True
    elif dtype == 'label':
        if not re.match(f'^{CoreData.REG_TYPE["label"]}$', value):
            return True
    elif dtype == 'float':
        if not re.match(f'^({CoreData.REG_TYPE["float"]}|{CoreData.REG_TYPE["float_hex"]})$', value):
            return True
    elif dtype == 'int':
        if not re.match(f'^{CoreData.REG_TYPE["int"]}$', value):
            return True
    return False

def xml_format_validation(path: str):
    """Check if XML file is well-formed

    Terminate program with code ErrorCode.XML_FORMAT_ERROR
    when error occure.

    Parameters:
    path (str): Path to XML file

    """
    parser = make_parser()
    parser.setContentHandler(ContentHandler())
    try:
        parser.parse(path)
    except:
        ErrorCode.exit_error(f"XML file '{path}' is not well-formed!",
                             ErrorCode.XML_FORMAT_ERROR)


def root_element_validation(root: ET.Element) -> bool:
    """Check root element struction

    Parameters:
    root (ET.Element):  Root element

    Returns:
    bool: True if error occured otherwise return False

    """
    # check root tag
    if root.tag != 'program':
        return True
    language = root.get('language')
    if language is None or language != 'IPPcode22':
        return True
    return False

def inst_element_validation(inst: ET.Element, order_used: list) -> (str, int):
    """Check element 'instruction' structure 

    Terminate program with code ErrorCode.XML_STRUCTURE_ERROR
    when error occure.

    Parameters:
    inst (ET.Element):  Instruction element
    order_used (list):  List of order values that have been already used

    Returns:
    str, int: Extracted values from inst element

    """
    if inst.tag != 'instruction':
        ErrorCode.exit_error(
                f"""Error occured while loading instruction element:
Expected element tag: instruction
Received element tag: {inst.tag}""",
                ErrorCode.XML_STRUCTURE_ERROR)

    if inst.get('opcode') is None:
        ErrorCode.exit_error(
                """Error occured while loading instruction element:
Missing attribute 'opcode'!""",
                ErrorCode.XML_STRUCTURE_ERROR)
    # formatting code for later use
    opcode = inst.get('opcode').upper()
    if instruct_set.get(opcode) is None:
        ErrorCode.exit_error(
                f"""Error occured while loading instruction element:
Undefined operation code {opcode}""",
                ErrorCode.XML_STRUCTURE_ERROR)

    if inst.get('order') is None:
        ErrorCode.exit_error(
                """Error occured while loading instruction element:
Missing attribute 'order'!""",
                ErrorCode.XML_STRUCTURE_ERROR)
    try:
        order = int(inst.get('order'))
    except:
        ErrorCode.exit_error(
                """Error occured while loading instruction element:
Wrong order data type, int value expected!""",
                ErrorCode.XML_STRUCTURE_ERROR)

    if order < 1:
        ErrorCode.exit_error(
                """Error occured while loading instruction element:
Value of attribute order is invalid!""",
                ErrorCode.XML_STRUCTURE_ERROR)
    order_used.append(order)

    return opcode, order

def argument_attr_check(table_args: dict) -> list:
    """Check 'args' elemet strucure

    After checking the validity of the table function sorts arguments from
    arg1 to arg3 depending on the size of the table.

    Terminate program with code ErrorCode.XML_STRUCTURE_ERROR
    when error occure.

    Parameters:
    table_args (dict):  List of arguments of the instruction
    """
    args_vals = []
    # validate args tags
    keys = table_args.keys()
    if ((len(keys) > 0 and 'arg1' not in keys) or
        (len(keys) > 1 and 'arg2' not in keys) or
        (len(keys) > 2 and 'arg3' not in keys)):
        ErrorCode.exit_error(
                """Error while loading argument elements:
Argument sequence is invalid""",
                ErrorCode.XML_STRUCTURE_ERROR)

    for key in sorted(table_args.keys()):
        args_vals.append(table_args[key])
    return args_vals


def xml_parser() -> list:
    """Full XML source file check

    Returns:
    list: List of (unsorted) loaded operations
    """

    lof_ins = []
    # TODO: check if file exists
    xml_path = sys.stdin if CoreData.source_file is None else CoreData.source_file
    xml_format_validation(xml_path)

    tree = ET.parse(xml_path)
    program = tree.getroot()
    # check root attributes
    if root_element_validation(program):
        ErrorCode.exit_error(
                "Error while loading root element",
                ErrorCode.XML_STRUCTURE_ERROR)

    order_numbers = []

    # loading operations
    for inst in program:
        opcode, order = inst_element_validation(inst, order_numbers)
        table_args   = {}

        # arguments check
        for args_element in inst:
            if not re.match("^arg[1-3]$", args_element.tag):
                ErrorCode.exit_error(
                        """Error while loading argument elements:
Invalid tag name, arg1/arg2/arg3 expected""",
                        ErrorCode.XML_STRUCTURE_ERROR)

            if format_validation(args_element.get('type'), args_element.text):
                ErrorCode.exit_error(
                        "Argument format error.",
                        ErrorCode.XML_STRUCTURE_ERROR)
            table_args[args_element.tag] = (args_element.get('type'), args_element.text)

        args = argument_attr_check(table_args)
        stat = Statement(opcode, order, args)
        CoreData.update_label_data(stat)
        lof_ins.append(stat)

    # check for jumps to undefined labels and duplicates
    if len(CoreData.undef_labels) > 0:
        # TODO: write output to stderr
        ErrorCode.exit_error(
                "Error: Source file contains undefined labels",
                ErrorCode.SEMANTIC_ERROR)
    if len(order_numbers) != len(set(order_numbers)):
        ErrorCode.exit_error(
                "Error: Duplicate order values found",
                ErrorCode.XML_STRUCTURE_ERROR)

    return lof_ins
