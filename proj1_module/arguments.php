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
     * Function goes through remaining arguments, validates the syntax
     * and creates instance of Stats for later source code processing.
     * 
     * @param args List of program arguments without first (executable file) argument
     * @return Stats Instance of Stats
     */
    private static function extract_stats_options($args)
    {
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
        Program slouzici k prepisu zdrojoveho kodu IPPcode22 do XML zapisu.
        Pouziti:
            php parser.php [--help]
            php parser.php [--stats=file1 OPTIONS_1] [--stats=file2 OPTIONS_2] ...

        Argumenty:
            --help          Vypis teto napovedy
            --stats=file    Vypis statistickych hodnot do souboru file
        
        Statisticka nastaveni:
            --loc           Pocet prikazu ve zdrojovem souboru
            --comments      Pocet komentari ve zdrojovem souboru
            --labels        Pocet navesti ve zdrojovem souboru
            --jumps         Pocet instrukci navratu z volani a instrukci pro skoky ve zdrojovem souboru
            --fwjumps       Pocet doprednych skoku
            --backjumps     Pocet zpetnych skoku
            --badjumps      Pocet skoku na neexistujici navesti

        Prikladna pouziti:
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
     * to determine what will output.
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
        // TODO: usage of -h option for help
        // if (in_array('--help', $args) || in_array('-h', $args))
        if (in_array('--help', $args))
        {
            if (count($args) > 1)
            {
                error_log("Spatna sekvence parametru! --help parametr nelze kombinovat s zadnym dalsim parametrem!");
                exit(ErrorCode::WRONG_PARAMS->value);
            }
            self::print_usage();
            exit(ErrorCode::NO_ERROR->value);
        }
        
        // list of arguments that don't start with --stats option is an error
        if (!preg_match("/^--stats/", $args[0]))
        {
            error_log("Spatna sekvence parametru! Pro vypis statistik musi sekce zacit parametrem --stats\nPro napovedu pouzij --help parametr");
            exit(ErrorCode::WRONG_PARAMS->value);
        }

        return self::extract_stats_options($args);
    }
}
/* arguments.php */
?>