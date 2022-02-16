<?php
/**
 * @brief File with constants
 *
 * This source code serves as submission for 
 * the first part of the project of class IPP at FIT, BUT 2021/2022
 * 
 * @file    constants.php
 * @author  Hung Do
 * @date    16.02.2022
 */

/** List of elementary regular expressions */
$REG_STR = array(
    'var'     => "(GF|LF|TF)@[a-zA-Z_$&%*!?-][a-zA-Z0-9_$&%*!?-]*",
    'str'     => '(string@(([^\s#\\\\]|\\\\\d{3})+|(?=\W|$)))',
    'int'     => "int@[-]?\d+",
    'bool'    => "bool@(true|false)",
    'nil'     => "nil@nil",
    'label'   => "\b[a-zA-Z]+\b",
    'type'    => "(int|bool|string)",
    'header'  => "\.IPPcode22",
    'comment' => "#.*"
);
$REG_STR['symb'] = "($REG_STR[var]|$REG_STR[str]|$REG_STR[int]|$REG_STR[bool]|$REG_STR[nil])";

/**
 * @brief Create instruction regex by concatenating elementary regex
 *
 * @param cmd   Instruction name
 * @param arg1  First argument (default value: null)
 * @param arg2  Second argument (default value: null)
 * @param arg3  Third argument (default value: null)
 */
function init_regex($cmd, $arg1=null, $arg2=null, $arg3=null)
{
    $delim = "\s+";
    $output = "/^(?i:$cmd)";

    // append arguments
    if (!is_null($arg1))
        $output .= $delim . $arg1;
    if (!is_null($arg2))
        $output .= $delim . $arg2;
    if (!is_null($arg3))
        $output .= $delim . $arg3;
    return $output . '\s*$/';
}

/** Instruction set with its regular expressions */
$INS_SET = array(
    'MOVE'        => init_regex("move", $REG_STR['var'], $REG_STR['symb']),
    'CREATEFRAME' => init_regex("createframe"),
    'PUSHFRAME'   => init_regex("pushframe"),
    'POPFRAME'    => init_regex("popframe"),
    'DEFVAR'      => init_regex("defvar", $REG_STR['var']),
    'CALL'        => init_regex("call", $REG_STR['label']),
    'RETURN'      => init_regex("return"),
                     
    'PUSHS'       => init_regex("pushs", $REG_STR['symb']),
    'POPS'        => init_regex("pops", $REG_STR['var']),
                     
    'ADD'         => init_regex("add", $REG_STR['var'], $REG_STR['symb'], $REG_STR['symb']),
    'SUB'         => init_regex("sub", $REG_STR['var'], $REG_STR['symb'], $REG_STR['symb']),
    'MUL'         => init_regex("mul", $REG_STR['var'], $REG_STR['symb'], $REG_STR['symb']),
    'IDIV'        => init_regex("idiv", $REG_STR['var'], $REG_STR['symb'], $REG_STR['symb']),
    'LT'          => init_regex("lt", $REG_STR['var'], $REG_STR['symb'], $REG_STR['symb']),
    'GT'          => init_regex("gt", $REG_STR['var'], $REG_STR['symb'], $REG_STR['symb']),
    'EQ'          => init_regex("eq", $REG_STR['var'], $REG_STR['symb'], $REG_STR['symb']),
    'AND'         => init_regex("and", $REG_STR['var'], $REG_STR['symb'], $REG_STR['symb']),
    'OR'          => init_regex("or", $REG_STR['var'], $REG_STR['symb'], $REG_STR['symb']),
    'NOT'         => init_regex("not", $REG_STR['var'], $REG_STR['symb']),
    'INT2CHAR'    => init_regex("int2char", $REG_STR['var'], $REG_STR['symb']),
    'STRI2INT'    => init_regex("stri2int", $REG_STR['var'], $REG_STR['symb'], $REG_STR['symb']),
                     
    'READ'        => init_regex("read", $REG_STR['var'], $REG_STR['type']),
    'WRITE'       => init_regex("write", $REG_STR['symb']),
                     
    'CONCAT'      => init_regex("concat", $REG_STR['var'], $REG_STR['symb'], $REG_STR['symb']),
    'STRLEN'      => init_regex("strlen", $REG_STR['var'], $REG_STR['symb']),
    'GETCHAR'     => init_regex("getchar", $REG_STR['var'], $REG_STR['symb'], $REG_STR['symb']),
    'SETCHAR'     => init_regex("setchar", $REG_STR['var'], $REG_STR['symb'], $REG_STR['symb']),
                     
    'TYPE'        => init_regex("type", $REG_STR['var'], $REG_STR['symb']),
                     
    'LABEL'       => init_regex("label", $REG_STR['label']),
    'JUMP'        => init_regex("jump", $REG_STR['label']),
    'JUMPIFEQ'    => init_regex("jumpifeq", $REG_STR['label'], $REG_STR['symb'], $REG_STR['symb']),
    'JUMPIFNEQ'   => init_regex("jumpifneq", $REG_STR['label'], $REG_STR['symb'], $REG_STR['symb']),
    'EXIT'        => init_regex("exit", $REG_STR['symb']),
                     
    'DPRINT'      => init_regex("dprint", $REG_STR['symb']),
    'BREAK'       => init_regex("break")
);

?>
