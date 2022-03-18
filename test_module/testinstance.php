<?php

class TestInstance
{
    public readonly string $test_name;
    public $ret_code;
    public $exp_ret_code;
    private $rc_log;
    private $output_log;
    public $output_result;
    public $output_file;

    public function __construct(string $test_name,
                                bool $output_result=null,
                                string $output_file=null)
    {
        $this->test_name     = $test_name;
        $this->ret_code      = 0;
        $this->exp_ret_code  = 0;
        $this->rc_log        = [];
        $this->output_log    = [];
        $this->output_result = $output_result;
        $this->output_file   = $output_file;
    }

    public function get_return_code()
    {
        return $this->ret_code == $this->exp_ret_code;
    }

    public function add_rc_log($content)
    {
        if (is_array($content))
            $content = implode("\n", $content);
        
        $content = str_replace("&", "&amp;", $content);
        $content = str_replace("<", "&lt;",  $content);
        $content = str_replace(">", "&gt;",  $content);
        $content = str_replace("\n", "<br/>\n", $content);
        array_push($this->rc_log, $content);
    }

    public function get_rc_log()
    {
        return implode("", $this->rc_log);
    }

    public function add_output_log($content)
    {
        if (is_array($content))
            $content = implode("\n", $content);
        
        $content = str_replace("&", "&amp;", $content);
        $content = str_replace("<", "&lt;",  $content);
        $content = str_replace(">", "&gt;",  $content);
        $content = str_replace("\n", "<br/>\n", $content);
        array_push($this->output_log, $content);
    }

    public function get_output_log()
    {
        return implode("", $this->output_log);
    }

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
