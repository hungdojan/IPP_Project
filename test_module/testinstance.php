<?php
/**
 * Class containing information about one test session
 *
 * This source code serves as submission for
 * second part of the project of class IPP at FIT, BUT 2021/2022
 *
 * @author  Hung Do
 */

class TestInstance
{
    public readonly string $test_name;
    public $ret_code;
    public $exp_ret_code;
    private $rc_log;
    private $output_log;
    public $output_result;
    public $output_file;

    /**
     * Class constructor
     * 
     * @param $test_name    Test session's name
     */
    public function __construct(string $test_name)
    {
        $this->test_name     = $test_name;
        $this->ret_code      = 0;
        $this->exp_ret_code  = 0;
        $this->rc_log        = [];
        $this->output_log    = [];
        $this->output_result = null;
        $this->output_file   = null;
    }

    /**
     * Get return code comparison result
     * 
     * @return bool 'true' when return code test passed
     */
    public function get_return_code()
    {
        return $this->ret_code == $this->exp_ret_code;
    }

    /**
     * Add line to return code log
     * When array of string if passed function join all the lines with newline (\n) symbol.
     * Then converts all special characters (<, >, &) to HTML safe strings (&gt;, &lt;, &amp;).
     * Newlines are also converted to HTML break elements <br/> (XML compatibility).
     * 
     * @param content Content of passing message
     */
    public function add_rc_log($content)
    {
        // joining array content
        if (is_array($content))
            $content = implode("\n", $content);
        
        // replacing special characters and newline symbols
        $content = str_replace("&", "&amp;", $content);
        $content = str_replace("<", "&lt;",  $content);
        $content = str_replace(">", "&gt;",  $content);
        $content = str_replace("\n", "<br/>\n", $content);

        array_push($this->rc_log, $content);
    }

    /**
     * Get log content in one string
     * 
     * @return string Return code log's content
     */
    public function get_rc_log()
    {
        return implode("", $this->rc_log);
    }

    /**
     * Add line to output log
     * When array of string if passed function join all the lines with newline (\n) symbol.
     * Then converts all special characters (<, >, &) to HTML safe strings (&gt;, &lt;, &amp;).
     * Newlines are also converted to HTML break elements <br/> (XML compatibility).
     * 
     * @param content Content of passing message
     */
    public function add_output_log($content)
    {
        // joining array content
        if (is_array($content))
            $content = implode("\n", $content);
        
        // replacing special characters and newline symbols
        $content = str_replace("&", "&amp;", $content);
        $content = str_replace("<", "&lt;",  $content);
        $content = str_replace(">", "&gt;",  $content);
        $content = str_replace("\n", "<br/>\n", $content);
        array_push($this->output_log, $content);
    }

    /**
     * Get log content in one string
     * 
     * @return string Return code log's content
     */
    public function get_output_log()
    {
        return implode("", $this->output_log);
    }

    /**
     * Get test session's result
     * 
     * @return bool 'true' if test was successful
     */
    public function get_test_result()
    {
        if ($this->ret_code != $this->exp_ret_code)
            return false;
        if ($this->ret_code)
            return true;
        if (is_null($this->output_result))
            return true;
        return $this->output_result;
    }
}

?>
