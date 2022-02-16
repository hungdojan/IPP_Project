<?php
/**
 * @brief Class Command representing one instruction in program
 *
 * This source code serves as submission for 
 * the first part of the project of class IPP at FIT, BUT 2021/2022
 * 
 * @file    command.php
 * @author  Hung Do
 * @date    16.02.2022
 */

/**
 * Class Command
 * @brief Abstract class of one instruction in program
 */
class Command
{
    public string $cmd;     ///< Instruction name
    public array $args;     ///< List of arguments

    public function __construct($input)
    {
        // remove newline character
        $input = trim($input);

        $cmd_data = preg_split("/\s+/", $input);
        if (count($cmd_data) > 0)
            $this->cmd  = strtoupper($cmd_data[0]);

        // load arguments
        $this->args = [];
        if (count($cmd_data) > 1)
            array_push($this->args, $cmd_data[1]);
        if (count($cmd_data) > 2)
            array_push($this->args, $cmd_data[2]);
        if (count($cmd_data) > 3)
            array_push($this->args, $cmd_data[3]);
    }

    /**
     * @brief Generate arguments in xmlwriter
     *
     * @param xw    Opened xmlwriter
     * @param data  Current argument
     * @param index Argument position
     */
    private function generate_arg_xml($xw, $data, $index)
    {
        global $REG_STR;
        // <argX>
        xmlwriter_start_element($xw, "arg$index");

        // get type and value
        if (preg_match("/^$REG_STR[var]$/", $data))
        {
            $type = 'var';
            $value = $data;
        }
        else if (preg_match("/^$REG_STR[type]$/", $data))
        {
            $type = 'type';
            $value = $data;
        }
        else if (preg_match("/^$REG_STR[label]$/", $data))
        {
            $type = 'label';
            $value = $data;
        }
        else
        {
            $tmp = explode("@", $data);
            $type = $tmp[0];
            $value = $tmp[1];
        }

        // replace problematic characters
        str_replace("&", "&amp", $data);
        str_replace("<", "&lt", $data);
        str_replace(">", "&gt", $data);

        // <argX type="XXX">
        xmlwriter_start_attribute($xw, 'type');
        xmlwriter_text($xw, "$type");
        xmlwriter_end_attribute($xw);

        // content
        xmlwriter_text($xw, "$value");

        // </argX>
        xmlwriter_end_element($xw);
    }

    /**
     * @brief Generate instruction in xmlwriter
     *
     * @param xw    Opened xmlwriter
     * @param order Number of order
     */
    public function generate_xml($xw, $order)
    {
        // <instruction>
        xmlwriter_start_element($xw, 'instruction');

        // <instruction order="XXX" opcode="XXX">
        xmlwriter_start_attribute($xw, 'order');
        xmlwriter_text($xw, "$order");
        xmlwriter_end_attribute($xw);

        xmlwriter_start_attribute($xw, 'opcode');
        xmlwriter_text($xw, "$this->cmd");
        xmlwriter_end_attribute($xw);

        // <argX type="XXX">XXX</argX>
        foreach ($this->args as $index => $item)
            $this->generate_arg_xml($xw, $item, $index+1);

        // </instruction>
        xmlwriter_end_element($xw);
    }

    public function __toString()
    {
        return $cmd . $args;
    }
}
?>
