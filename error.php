<?php
/**
 * @brief Enumeration of error codes
 *
 * This source code serves as submission for 
 * the first part of the project of class IPP at FIT, BUT 2021/2022
 * 
 * @file    error.php
 * @author  Hung Do
 * @date    16.02.2022
 */

/** 
 * enum ErrorCode
 * @brief Enumeration of error codes
 */
enum ErrorCode: int
{
    case NO_ERROR       =  0;   ///< no error

    case WRONG_PARAMS   = 10;   ///< unallowed combination of parameters
    case IN_FILE_ERROR  = 11;   ///< error while working with input file
    case OUT_FILE_ERROR = 12;   ///< error while working with output file

    case MISSING_HEADER = 21;   ///< missing header in source file
    case WRONG_COMMAND  = 22;   /// < unknown command in source code
    case UNDEF_LEX_OR_SYNTAX_ERROR = 23;    ///< other type of lexical or syntax error

    case UNDEFINED_ERROR = 99;  ///< other type of errors
}
?>
