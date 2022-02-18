<?php
/**
 * File contains main function _parser_ that does
 *  lexical and syntax analysis of the source file
 *
 * This source code serves as submission for 
 * the first part of the project of class IPP at FIT, BUT 2021/2022
 * 
 * @author  Hung Do
 */

require_once "error.php";
require_once "constants.php";
require_once "command.php";
require_once "stats.php";

/**
 * Lexical and syntax analysis of source file
 *
 * @param stats Instance of class Stats (default: null)
 * @return array List of loaded instructions
 */
function parser($stats=null)
{
    global $REG_STR, $INS_SET;
    $line = '';
    $lof_ins = [];
    $line_count = 0;

    $header = false;
    while ( ($line = fgets(STDIN)) )
    {
        $line_count++;
        $line = trim($line);
        if (preg_match("/$REG_STR[comment]/", $line))
        {
            // increment number of comments and remove it
            if (!is_null($stats))
                $stats->inc_comments();
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

        // header must appear before any instruction
        // only empty lines and comments are allowed appear before header
        if (!$header)
        {
            error_log("Chybi hlavicka .IPPcode22 ve zdrojovem kodu!");
            exit(ErrorCode::MISSING_HEADER->value);
        }

        // error validation variables
        $valid_cmd = false;
        $valid_syntax = false;
        foreach($INS_SET as $key => $value)
        {
            // instruction validation
            if (preg_match("/^(?i:$key)(\s|$)/", $line))
                $valid_cmd = true;

            // whole line validation (lexical and syntax)
            if (preg_match($value, $line))
            {
                $command = new Command($line);

                // add instruction to list and continue to next instruction
                array_push($lof_ins, $command);
                if (!is_null($stats))
                    $stats->loc_analysis($command);

                $valid_syntax = true;
                break;
            }
        }
        // error checking
        if (!$valid_cmd)
        {
            error_log("Neznama instrukce!\n\n----- Radek $line_count -----\n$line");
            exit(ErrorCode::WRONG_COMMAND->value);
        }
        if (!$valid_syntax)
        {
            error_log("Chybna syntaxe!\n\n----- Radek $line_count -----\n$line");
            exit(ErrorCode::UNDEF_LEX_OR_SYNTAX_ERROR->value);
        }
    }
    return $lof_ins;
}
/* lex_and_parse.php */
?>
