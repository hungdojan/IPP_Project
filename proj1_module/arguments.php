<?php
/**
 * File contains function that handle program arguments
 *
 * This source code serves as submission for 
 * the first part of the project of class IPP at FIT, BUT 2021/2022
 * 
 * @author  Hung Do
 */

require_once "error.php";
require_once "constants.php";
require_once "stats.php";

class Arguments
{
    /// List of permitted flags used with --stats flag
    private static $PERMITTED_STATS_FLAGS = [
        '--loc', '--comments','--labels', '--jumps', '--fwjumps', '--backjumps', '--badjumps'
    ];

    /**
     * Extraction of stats options
     * 
     * New instance of Stats is initialized.
     * Function divides array of arguments into smaller sections where
     * each section starts with '--stats' option. Then are validated within sections.
     * Program is terminated with return code 10 when user used undefined option.
     *
     * Section is added to the Stats instance. After function successfully
     * cycle through all section, object Stats is returned.
     * 
     * @param args List of program arguments without first (executable file) argument
     * @return Stats Instance of Stats
     */
    private static function extract_stats_options($args)
    {
        // create regular expression by joining PERMITED_FLAGS with '|' sign
        $REGEX_FLAGS = implode('|', self::$PERMITTED_STATS_FLAGS);
        $option = getopt("", ['stats:']);   // for file name extraction
        // position of --stats option in $args
        $indices = array_keys(array_filter($args, function($var) {
            return preg_match("/^--stats/", $var);
        }));
        array_push($indices, count($args));

        $stats = new Stats();

        // append each section of stats option to $stats
        foreach (range(0, count($indices)-2) as $i)
        {
            // one selection of options
            $stats_section = array_slice($args, $indices[$i], $indices[$i+1]);

            // extract output file path
            // and remove --stats option with its parameter (file name)
            $filename = $option['stats'][$i];
            if (preg_match("/^--stats=/", $stats_section[0]))
                $stats_section = array_splice($stats_section, 1, count($stats_section));
            else
                $stats_section = array_splice($stats_section, 2, count($stats_section));
            

            // extract options
            $stats_options = [];
            foreach ($stats_section as $opt)
            {
                // validate options
                if (!preg_match("/^($REGEX_FLAGS)$/", $opt))
                {
                    error_log("Unknown argument used! Option \"$opt\" is not defined!\nFor help use --help option");
                    exit(ErrorCode::WRONG_PARAMS->value);
                }
                // remove "--" from the beginning of the option
                // and push it into $stats_options
                array_push($stats_options, preg_replace("/^--/", "", $opt));
            }
            $stats->append_stats_instance($stats_options, $filename);
        }
        return $stats;
    }

    /**
     * Print usage to stdin
     */
    private static function print_usage()
    {
        // TODO: usage of -h option for help
        $usage_msg = <<<EOT
        Program converts IPPcode22 source file into XML representation for interpret.py
        usage:  php parser.php [--help]
                php parser.php [--stats=file1 OPTIONS_1] [--stats=file2 OPTIONS_2] ...
                    - OPTIONS_n is list of stats options

        options:
            --help          show this help message and exit
            --stats=file    creates output file with statistics;
                            file - output file name

        Each statistics options starts with --stats flag with defined output file path.
        After initial --stats flag follows list of statistics flags (list of available
        flags are written in the next section underneath block). To initialize new statistics add new --stats flag.

        stats flags:
            --loc           lines of code
            --comments      number of lines with comments
            --labels        number of labels
            --jumps         number of jumps, call and returns
            --fwjumps       number of forward jumps
            --backjumps     number of backward jumps
            --badjumps      number of jumps to undefined labels

        examples:
            php parser.php --help
            php parser.php --stats=file.txt --loc --comments < intput > output
            php parser.php --stats=file1 --loc --stats=file2 --comments\n
        EOT;
        echo $usage_msg;
    }

    /**
     * Arguments processing
     * 
     * Given parameters $argc and $argv, function processes program arguments
     * to determine what will be outputed.
     * 
     * @param argc Number of arguments (equals global $argc)
     * @param argv List of arguments (equals global $argv)
     * @return Stats When stats option is provided function returns instance of Stats otherwise null
     */
    public static function process_args($argc, $argv)
    {
        // remomve first argument
        $args = array_slice($argv, 1, $argc);

        // no argument
        if (count($args) == 0)
            return null;

        // help option
        // no other option must be present
        if (in_array('--help', $args))
        {
            if (count($args) > 1)
            {
                error_log("Wrong sequence of options! --help option cannot be combined with other options!");
                exit(ErrorCode::WRONG_PARAMS->value);
            }
            self::print_usage();
            exit(ErrorCode::NO_ERROR->value);
        }
        
        // list of arguments that don't start with --stats option is an error
        if (!preg_match("/^--stats/", $args[0]))
        {
            error_log("Wrong sequence of options! Every statistics instance should start with --stats option\n".
                "For help use --help option");
            exit(ErrorCode::WRONG_PARAMS->value);
        }

        return self::extract_stats_options($args);
    }
}
/* arguments.php */
?>
