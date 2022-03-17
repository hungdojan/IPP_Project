<?php

class TestInstance
{
    public readonly string $test_name;
    public readonly int $ret_code;
    public readonly int $exp_ret_code;
    public readonly ?bool $output_result;
    public readonly ?string $output_file;
    public readonly ?string $other_log;

    public function __construct(string $test_name,
                                int $ret_code,
                                int $exp_ret_code,
                                bool $output_result=null,
                                string $output_file=null,
                                string $other_log=null)
    {
        $this->test_name     = $test_name;
        $this->ret_code      = $ret_code;
        $this->exp_ret_code  = $exp_ret_code;
        $this->output_result = $output_result;
        $this->output_file   = $output_file;
        $this->other_log     = $other_log;
    }

    public function get_return_code()
    {
        return $this->ret_code == $this->exp_ret_code;
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
