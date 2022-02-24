"""ErrorCode static class with enums of error codes

Author: Hung Do
File:   error.py
Module: proj2_module
"""
import sys

class ErrorCode:
    XML_FORMAT_ERROR = 31
    XML_STRUCTURE_ERROR = 32

    SEMANTIC_ERROR = 52
    RUNTIME_WRONG_TYPE = 53
    RUNTIME_UNDEF_VAR = 54
    RUNTIME_NONEXIST_FRAME = 55
    RUNTIME_MISSING_VALUE = 56
    RUNTIME_WRONG_VALUE = 57
    RUNTIME_STRING_HANDLING = 58

    UNDEFINED_ERROR = 99

    @staticmethod
    def exit_error(msg: str, error_code: int):
        """Print error message to stderr and terminate program with given value

        Parameters:
        msg (str):          Error message
        error_code (int):   Error code

        """
        sys.stderr.write(msg)
        sys.stderr.write('\n')
        sys.exit(error_code)

