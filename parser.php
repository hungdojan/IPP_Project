<?php
/**
 * @brief Main file
 *
 * This source code serves as submission for 
 * the first part of the project of class IPP at FIT, BUT 2021/2022
 * 
 * @file    parser.php
 * @author  Hung Do
 * @date    16.02.2022
 */

require_once 'lex_and_parse.php';

/**
 * @brief Generates list of instructions to XML
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
// TODO: arguments handling
$lof_ins = parser();
ins_to_xml($lof_ins);

?>
