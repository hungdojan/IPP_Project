<?php
/**
 * @brief File contains main function _parser_ that does
 *  lexical and syntax analysis of the source file
 *
 * This source code serves as submission for 
 * the first part of the project of class IPP at FIT, BUT 2021/2022
 * 
 * @file    lex_and_parse.php
 * @author  Hung Do
 * @date    16.02.2022
 */

require_once "error.php";
require_once "constants.php";
require_once "command.php";
require_once "stats.php";

/**
 * @brief Lexical and syntax analysis of source file
 *
 * @return List of loaded instructions
 */
function parser()
{
    global $REG_STR, $INS_SET;
    $line = '';
    $lof_ins = [];

    $header = false;
    while ( ($line = fgets(STDIN)) )
    {
        $line = trim($line);
        if (preg_match("/$REG_STR[comment]/", $line))
        {
            // TODO: stats
            $line = preg_replace("/$REG_STR[comment]/", "\n", $line);
        }

        // empty line
        if (preg_match("/^\s*$/", $line))
            continue;

        // check for header
        if (preg_match("/$REG_STR[header]/", $line))
        {
            $header = true;
            continue;
        }

        // error validation variables
        $valid_cmd = false;
        $valid_syntax = false;
        foreach($INS_SET as $key => $value)
        {
            // instruction validation
            if (preg_match("/^(?i:$key)/", $line))
                $valid_cmd = true;

            // whole line validation (lexical and syntactic)
            if (preg_match($value, $line))
            {
                // add instruction to list and continue to next instruction
                array_push($lof_ins, new Command($line));
                $valid_syntax = true;
                break;
            }
        }
        // error checking
        if (!$header)
            exit(ErrorCode::MISSING_HEADER->value);
        if (!$valid_cmd)
            exit(ErrorCode::WRONG_COMMAND->value);
        if (!$valid_syntax)
            exit(ErrorCode::UNDEF_LEX_OR_SYNTAX_ERROR->value);
    }
    return $lof_ins;
}
?>
