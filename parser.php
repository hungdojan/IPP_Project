<?php
/**
 * Main file
 *
 * This source code serves as submission for 
 * the first part of the project of class IPP at FIT, BUT 2021/2022
 * 
 * @author  Hung Do
 */

require_once 'php/lex_and_parse.php';
require_once 'php/arguments.php';

// output error messages to stderr
ini_set('display_errors', 'stderr');

/**
 * Generates list of instructions to XML
 *
 * @param lof_ins   List of instruction
 */
function ins_to_xml($lof_ins)
{
    $xw = xmlwriter_open_memory();
    xmlwriter_set_indent($xw, true);
    $res = xmlwriter_set_indent_string($xw, '  ');

    // header
    xmlwriter_start_document($xw, '1.0', 'UTF-8');

    // <program language="IPPcode22">
    xmlwriter_start_element($xw, 'program');
    xmlwriter_start_attribute($xw, 'language');
    xmlwriter_text($xw, 'IPPcode22');
    xmlwriter_end_attribute($xw);

    foreach($lof_ins as $index => $item)
        $item->generate_xml($xw, $index+1);

    // </program>
    xmlwriter_end_element($xw);
    echo xmlwriter_output_memory($xw);
}


// main function
$stats = Arguments::process_args($argc, $argv);
$lof_ins = parser($stats);
ins_to_xml($lof_ins);
if (!is_null($stats))
    $stats->flush_files();

/* parser.php */
?>
