<?php
/**
 * Class StatsFile and Stats for outputing statistics about source code
 *
 * This source code serves as submission for 
 * the first part of the project of class IPP at FIT, BUT 2021/2022
 * 
 * @author  Hung Do
 */

require_once 'error.php';

/**
 * Class Stats
 * Static class with all available stats value of the source code
 */
class Stats
{
    private $loc        = 0;    ///< line of code counter
    private $comments   = 0;    ///< comment counter
    private $labels     = 0;    ///< (unique) label counter
    private $jumps      = 0;    ///< jump counter
    private $fwjumps    = 0;    ///< jump forward counter
    private $backjumps  = 0;    ///< jump back counter
    private $badjumps   = 0;    ///< jump to undefined label counter

    private $lof_files = [];        ///< list of asked stats file
    private $used_file_names = [];  ///< list of used stats file path

    // Label arrays
    private $defined_lbl = [];      ///< list of defined labels
    private $undefined_lbl = [];    ///< list of undefined labels with call counter

    /**
     * @breif Constructor of the class Stats
     */
    public function __construct() { }

    public function __get($name)
    {
        switch($name)
        {
            case 'loc':         return $this->loc;
            case 'comments':    return $this->comments;
            case 'labels':      return $this->labels;
            case 'jumps':       return $this->jumps;
            case 'fwjumps':     return $this->fwjumps;
            case 'backjumps':    return $this->backjumps;
            case 'badjumps':    return $this->badjumps;
            default:
                throw new OutOfBoundsException('Member is not gettable');
        }
    }

    /**
     * Increases comment counter
     */
    public function inc_comments()
    {
        $this->comments++;
    }

    /**
     * Push new instance of StatsFile to $lof_files
     *
     * Check if file_path (output file destination) is unique.
     * If not exit with given error code.
     *
     * @param $flags List of chosen flags
     * @param file_name Output fil destination
     */
    public function append_stats_instance(array $flags, string $file_path)
    {
        // checks whether file_path is already in use
        if (in_array($file_path, $this->used_file_names))
        {
            error_log("File $file_path is already in use");
            exit(ErrorCode::OUT_FILE_ERROR->value);
        }

        // array_push($lof_files, new StatsFile($flags, $file_path));
        $this->lof_files[$file_path] = $flags;
        array_push($this->used_file_names, $file_path);
    }

    /**
     * Evaluates line of code to increment counter values
     *
     * Used for statistics
     *
     * @param command Object of class Command; one instruction of the program
     */
    public function loc_analysis($command)
    {
        if (!strcasecmp($command->ins, 'label'))
        {
            $label = $command->args[0]->value;
            if (in_array($label, array_keys($this->undefined_lbl)))
            {
                // update fwjumps and badjumps by the number of label calls
                $this->fwjumps += $this->undefined_lbl[$label];
                $this->badjumps -= $this->undefined_lbl[$label];

                // move new label from undefined to defined array
                array_push($this->defined_lbl, $label);
                unset($this->undefined_lbl[$label]);
                $this->labels++;
            }

            // new label
            elseif (!in_array($label, $this->defined_lbl))
            {
                array_push($this->defined_lbl, $label);
                $this->labels++;
            }
        }
        // jumps
        elseif (preg_match("/^return/i", $command->line))
            $this->jumps++;
        elseif (preg_match("/^(jump|jumpifeq|jumpifneq|call)/i", $command->ins))
        {
            $label = $command->args[0]->value;
            // already defined label
            if (in_array($label, $this->defined_lbl))
                $this->backjumps++;

            // for undefined label
            $this->badjumps++;
            if (in_array($label, $this->undefined_lbl))
                $this->undefined_lbl[$label]++;
            else
                $this->undefined_lbl[$label] = 1;

            $this->jumps++;
        }
        $this->loc++;
    }

    /**
     * Creates all statistic files
     */
    public function flush_files()
    {
        // Go through $this->files
        // and creates a file for each of stats
        foreach ($this->lof_files as $path => $flags)
        {
            if ( !($file = fopen($path, "w")) )
            {
                error_log("Error while accessing file $path");
                exit(ErrorCode::UNDEFINED_ERROR->value);
            }

            foreach ($flags as $flag)
            {
                fwrite($file, $this->$flag);
                fwrite($file, "\n");
            }
            fclose($file);
        }
    }
}
/* stats.php */
?>
