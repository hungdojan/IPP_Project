<?php
/**
 * Classes Command and CommandArgument representing instructions in program
 *
 * This source code serves as submission for 
 * the first part of the project of class IPP at FIT, BUT 2021/2022
 * 
 * @file    command.php
 * @author  Hung Do
 * @date    16.02.2022
 */

/**
 * Class CommandArgument
 * Class of one argument in instruction
 */
class CommandArgument
{
    private $type;
    private $value;

    public function __construct($type, $value)
    {
        $this->type = $type;
        $this->value = $value;
    }

    public function __get($name)
    {
        switch($name)
        {
        case 'type': return $this->type;
        case 'value': return $this->value;
        }
    }
}

/**
 * Class Command
 * Class of one instruction in program
 */
class Command
{
    public string $ins;     ///< Instruction name
    public array $args;     ///< List of arguments

    public function __construct($input)
    {
        // remove newline character
        $input = trim($input);

        $ins_data = preg_split("/\s+/", $input);
        if (count($ins_data) > 0)
            $this->ins  = strtoupper($ins_data[0]);

        // load arguments
        $this->args = [];
        if (count($ins_data) > 1)
            $this->extract_data($ins_data[1]);
        if (count($ins_data) > 2)
            $this->extract_data($ins_data[2]);
        if (count($ins_data) > 3)
            $this->extract_data($ins_data[3]);
    }

    /**
     * Convert string to CommandArgument
     * 
     * Newly created instance of CommandArgument
     * is push to array $this->args. 
     * It's a part of preparation for generating XML file
     *
     * @param data Argument string; must be trimmed beforehand
     */
    private function extract_data($data)
    {
        global $REG_STR;
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
        else if (preg_match("/^$REG_STR[str]$/", $data))
        {
            $type = 'string';
            $value = preg_replace("/^string@/", "", $data);
        }
        else
        {
            $tmp = explode("@", $data);
            $type = $tmp[0];
            $value = $tmp[1];
        }
        array_push($this->args, new CommandArgument($type, $value));
    }

    /**
     * Generate instruction in xmlwriter
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
        xmlwriter_text($xw, "$this->ins");
        xmlwriter_end_attribute($xw);

        // <argX type="XXX">XXX</argX>
        foreach ($this->args as $index => $item)
        {
            $index += 1;
            $value = $item->value;

            // <argX>
            xmlwriter_start_element($xw, "arg$index");

            // replace problematic characters
            str_replace("&", "&amp", $value);
            str_replace("<", "&lt", $value);
            str_replace(">", "&gt", $value);

            // <argX type="XXX">
            xmlwriter_start_attribute($xw, 'type');
            xmlwriter_text($xw, "$item->type");
            xmlwriter_end_attribute($xw);

            // content
            xmlwriter_text($xw, "$value");

            // </argX>
            xmlwriter_end_element($xw);
        }

        // </instruction>
        xmlwriter_end_element($xw);
    }

    public function __toString()
    {
        return $this->ins . $this->args;
    }
}
?>
