<?php
/**
 * HTML generating class
 *
 * This source code serves as submission for
 * second part of the project of class IPP at FIT, BUT 2021/2022
 *
 * @author  Hung Do
 */

require_once "testinstance.php";
require_once "html_templates.php";

class HtmlGenerator
{
    private static $instance = null;
    private $doc;   /**< DOMDocument */
    private $body;  /**< HTML <body> element */

    private function __construct()
    {
        // document setup
        $this->doc = new DOMDocument();
        $this->setup();
    }

    /**
     * Final HTML file setup
     * Stores important body elements for later easy access.
     */
    private function setup()
    {
        $this->doc->formatOutput = true;
        $this->doc->loadHTML(HtmlTemplates::get_body());
        $this->body = $this->doc->getElementsByTagName('body')->item(0);
    }

    /**
     * Get instance of HtmlGenerator
     * 
     * @return HtmlGenerator One instance of HtmlGenerator
     */
    public static function get_instance()
    {
        if (is_null(self::$instance))
            self::$instance = new self();
        return self::$instance;
    }

    /**
     * Get result's paragraph content
     * 
     * @return string Result paragraph's inner text
     */
    private function get_result_paragraph(TestInstance $test_instance)
    {
        // get test outcomes 
        $return_code_text = $test_instance->get_return_code() ?
                            "OK" : "FAILED";
        if (is_null($test_instance->output_result))
            $output_cmp_text = "SKIPPED";
        elseif($test_instance->output_result)
            $output_cmp_text = "OK";
        else
            $output_cmp_text = "FAILED";

        $output_msg = "Return code: <b>{$return_code_text}</b><br/>\n";
        $output_msg .= "Output comparison: <b>{$output_cmp_text}</b><br/>\n";

        // add link to output file when exists
        if (!is_null($test_instance->output_file))
            $output_msg .= "Output file: <a href=\"{$test_instance->output_file}\">See output file</a><br/>\n";
        return $output_msg;
    }

    /**
     * Load log content from test session
     * 
     * @param test_instance Instance of test session
     * @return string Log paragraph's inner text
     */
    private function get_log_paragraph($test_instance)
    {
        $rc_msg = $test_instance->get_rc_log();
        $output_msg = $test_instance->get_output_log();
        $output = $rc_msg;

        // return code and output comparison splitter
        $output .= "===============================<br/><br/>";

        if (!is_null($test_instance->output_result))
            $output .= $output_msg;
        return $output;
    }

    /**
     * Append new test session block to <body>
     * 
     * @param test_instance Instance of test session
     */
    public function add_test_instance($test_instance)
    {
        // choose test output depending on test result
        $doc = new DOMDocument();
        if ($test_instance->get_test_result())
            $doc->loadXML(HtmlTemplates::$test_passed);
        else
            $doc->loadXML(HtmlTemplates::$test_failed);

        $div = $doc->documentElement;
        // set test name 
        $h2 = $div->childNodes[1];
        $h2->nodeValue = $test_instance->test_name;

        // set test content (message)
        $p_res = $div->childNodes[3]->childNodes[1]->childNodes[1];
        $inner_text = $doc->createDocumentFragment();
        $inner_text->appendXML($this->get_result_paragraph($test_instance));
        $p_res->appendChild($inner_text);

        // log content
        $p_log = $div->childNodes[3]->childNodes[1]->childNodes[3];
        $log_text = $doc->createDocumentFragment();
        $log_text->appendXML($this->get_log_paragraph($test_instance));
        $p_log->appendChild($log_text);

        $this->body->appendChild($this->doc->importNode($div, true));
        
    }

    /**
     * Append final result block to <body>
     * 
     * @param nof_passed    Number of passed tests
     * @param nof_tests     Number of tests
     */
    public function generate_results($nof_passed, $nof_tests)
    {
        $doc = new DOMDocument();
        $nof_failed = $nof_tests - $nof_passed;
        $percentage_val = intval($nof_passed / $nof_tests * 100);
        if ($percentage_val >= 75)
            $color = HtmlTemplates::$colors['green'];
        elseif ($percentage_val >= 50)
            $color = HtmlTemplates::$colors['yellow'];
        elseif ($percentage_val >= 25)
            $color = HtmlTemplates::$colors['orange'];
        else
            $color = HtmlTemplates::$colors['red'];

        $doc->loadXML(HtmlTemplates::$test_results);
        $div = $doc->documentElement;

        $div->setAttribute('style', "background: $color");
        $percentage = $div->childNodes[3]->childNodes[3]->childNodes[1];
        $p = $div->childNodes[3]->childNodes[1]->childNodes[1];

        // text content
        $text_content = <<<EOT
        Tests passed: <b>{$nof_passed}</b><br/>
        Tests failed: <b>{$nof_failed}</b><br/>
        Number of tests: <b>{$nof_tests}</b>
        EOT;
        $inner_text = $doc->createDocumentFragment();
        $inner_text->appendXML($text_content);
        $p->appendChild($inner_text);

        // percentage
        $percentage->appendChild($doc->createTextNode("$percentage_val %"));
        // $percentage->setAttribute('style', "color: $color");

        $this->body->appendChild($this->doc->importNode($div, true));
    }

    /**
     * Print out file(s)
     * When output file is defined HTML content is parse into it.
     * Otherwise HTML content is printed to console.
     * 
     * @param file Output filename (default: null)
     */
    public function generate_files($file=null)
    {
        // generate html file
        if (is_null($file))
            echo $this->doc->saveHTML();
        else
            file_put_contents($file, $this->doc->saveHTML());
    }
}

/* html_generator.php */
?>
