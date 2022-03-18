<?php
/**
 * File with arguments processing
 *
 * This source code serves as submission for
 * second part of the project of class IPP at FIT, BUT 2021/2022
 *
 * @author  Hung Do
 */

/**
 * Write to stdout and append to msg to log file
 *
 * @param msg           Output content
 * @param logfilepath   Path to log file
 * @param write_stderr  Redirect msg to stderr
 */
function echo_log($msg, $logfilepath, $write_stderr=false)
{
    if (is_array($msg))
        $output_msg = implode("\n", $msg);
    else
        $output_msg = $msg;

    if ($write_stderr)
        error_log($output_msg);
    else
        echo $output_msg;
    file_put_contents($logfilepath, $output_msg, FILE_APPEND);
}

/**
 * Recursively remove directory content
 *
 * @param src_dir   Source directory
 */
function clean_directory($src_dir)
{
    if ($src_dir == '' || $src_dir == null)
        return;
    // recursively remove directory contents and directory
    $dirs = glob("$src_dir/*", GLOB_ONLYDIR);
    foreach ($dirs as $dir)
    {
        clean_directory($dir);
        rmdir($dir);
    }
    // remove files
    $files = glob("$src_dir/*");
    foreach ($files as $file)
        unlink($file);
}

class TestInfo
{
    // public const PHP_EXEC = 'php8.1';
    // public const PY_EXEC  = 'python3;
    public const PHP_EXEC = 'php';
    public const PY_EXEC  = 'python';
    private $logfile;

    // argument options
    public $directory;
    public $parse_script;
    public $int_script;
    public $jexampath;

    // toggle options
    public $recursive;
    public $parse_only;
    public $int_only;
    public $no_clean;

    public $nof_tests = 0;
    public $nof_passed = 0;

    /**
     * Class constructor
     *
     * @param output_dir    Path to test output directory 
     */
    public function __construct($output_dir)
    {
        // init test directory
        if (!is_dir($output_dir))
            mkdir($output_dir);
        else
            clean_directory($output_dir);

        $this->logfile = $output_dir."/init_test.log";
        $this->process_arguments();
    }

    /**
     * Validate sequence of options combined with --parse-only and file accessibility.
     * User is forbidden to combine --parse-only with --int options.
     * When user doesn't specify path to parse script program searches for 
     * parse script in current directory.
     *
     * When wrong sequence of options or invalid script path is given
     * program is terminated with error code 41.
     */
    private function check_parse_only()
    {
        // validate sequence of options
        if (!is_null($this->int_script) || $this->int_only)
        {
            echo_log("Invalid use of options\n".
                "--parse-only option cannot be combined with --int-script and --int-only options\n".
                "For help use --help option", $this->logfile, true);
            exit(41);
        }
        // assign default file path when user doesn't specify script's path
        if (is_null($this->parse_script))
            $this->parse_script = getcwd()."/parse.php";

        // validate file's existence
        if (!is_file($this->parse_script))
        {
            echo_log("Parse script not found!\nFor help use --help option",
                $this->logfile, true);
            exit(41);
        }

        // set default path to directory containing JExamXML
        // when no arguments were given
        // this default location is bound to school server merlin.fit.vutbr.cz
        $this->jexampath = $this->jexampath ?? "/pub/courses/ipp/jexamxml/";
        if (!preg_match('/\/$/', $this->jexampath))
            $this->jexampath .= '/';


        // check jexamxml.jar and option files
        if (!is_dir($this->jexampath))
        {
            echo_log("$this->jexampath path doesn't exist\nFor help use --help option",
                $this->logfile, true);
            exit(41);
        }
        if (!is_file($this->jexampath."jexamxml.jar") ||
            !is_file($this->jexampath."options"))
        {
            echo_log("Missing 'jexamxml.jar' or 'options' files in $this->jexampath\n".
                "For help use --help option", $this->logfile, true);
            exit(41);
        }
    }

    /**
     * Validate int-only tests
     * No parse related flags must be used in arguments together with int-only flag.
     * Otherwise program is terminated with error code 41.
     * 
     * Function also sets default values of $int_script if not specified by user.
     * When interpreter script not found, program is terminated with error code 41.
     */
    private function check_int_only()
    {
        // validate sequence of options
        if ($this->int_only && (!is_null($this->parse_script) ||
            $this->parse_only || !is_null($this->jexampath)))
        {
            echo_log("Invalid use of options\n".
                "--int-only option cannot be combined with --parse type of options and --jexampath\n".
                "For help use --help option", $this->logfile, true);
            exit(41);
        }

        // set default value when no argument was given
        // and check file's existence
        if (is_null($this->int_script))
            $this->int_script = getcwd()."/interpret.py";

        if (!is_file($this->int_script))
        {
            error_log("Interpret script not found!\nFor help use --help option",
                $this->logfile, true);
            exit(41);
        }
    }

    /**
     * Validate program arguments when neither --int-only nor --parse-only flags were defined.
     * 
     * Program is terminated with error code 41
     * if at least one of the scripts is invalid.
     */
    private function check_both()
    {
        // set default values when no arguments were given
        // and check their existence
        if (is_null($this->parse_script))
            $this->parse_script = getcwd()."/parse.php";
        if (is_null($this->int_script))
            $this->int_script = getcwd()."/interpret.py";

        if (!is_file($this->parse_script))
        {
            echo_log("Parse script not found!\nFor help use --help option",
                $this->logfile, true);
            exit(41);
        }

        if (!is_file($this->int_script))
        {
            error_log("Interpret script not found!\nFor help use --help option",
                $this->logfile, true);
            exit(41);
        }
    }

    /**
     * Validate arguments and their additional datas
     * Terminate program with return code 41 when files or directories paths are
     * not accessible or lead to non-existing files
     */
    private function arguments_validation()
    {
        if ($this->parse_only)
            $this->check_parse_only();
        elseif ($this->int_only)
            $this->check_int_only();
        else
            $this->check_both();
    }

    /**
     * Process program arguments using getopt function
     */
    public function process_arguments()
    {
        // array of long options
        $long_options = [
            "help", "directory:", "recursive", "parse-script:",
            "int-script:", "parse-only", "int-only", "jexampath:",
            "noclean"
        ];
        $options = getopt("", $long_options);

        // help flag
        // when valid prints usage and ends program
        if (array_key_exists("help", $options))
        {
            if (count($options) > 1)
            {
                error_log("Invalid sequence of options\n".
                    "--help option cannot be combined with other options");
                exit(10);
            }
            $this->print_help();
        }

        // path arguments
        // by default script searches 
        // these paths are set specifically for school server merlin.fit.vutbr.cz
        // optional:
        $this->directory    = $options['directory'] ?? getcwd();
        $this->jexampath    = $options['jexampath'] ?? null;
        $this->parse_script = $options['parse-script'] ?? null;
        $this->int_script   = $options['int-script'] ?? null;

        // true-false flags
        // when user sets these flags PHP store 'false' to $options[#flag#]
        // when flag is not set the stored value is null
        //
        // in order to set flag's value, true value is assigned when user doesn't
        // toggle the flag with null coalescing operator (??)
        // and then the final value is negated
        $this->recursive    = ! ($options['recursive']  ?? true);
        $this->parse_only   = ! ($options['parse-only'] ?? true);
        $this->int_only     = ! ($options['int-only']   ?? true);
        $this->no_clean     = ! ($options['noclean']    ?? true);
        $this->arguments_validation();
    }

    /**
     * Function prints program usage onto stdout
     * and ends program afterwards.
     */
    public static function print_help()
    {
        $usage_msg = <<<EOT
        IPPcode22 interpreter testing script
        usage: test.php [--help]
               test.php [--directory dir] [--recursive] [jexampath dir] [--noclean]
               test.php [--parse-script filename] [--parse-only]
               test.php [--int-script filename] [--int-only]

        options:
            --help                   show this help message and exit
            --directory dir          (optional) directory name with test files
                                     (default: current directory)
            --recursive              recursively run tests in subdirectories
            --parse-script filename  (optional) path to parse PHP script
                                     (default: searches for script in current directory)
            --parse-only             run only tests with parse scipt
                                     cannot be combined with: --int-only, --int-script
            --int-script filename    (optional) path to interpret Python script
                                     (default: searches for script in current directory)
            --int-only               run only tests with interpret scipt
                                     cannot be combined with: --parse-only, --int-script, --jexampath
            --jexampath dir          (optional) path to directory containing jexamxml.jar
                                     and options files (default: /pub/courses/ipp/jexamxml/)
            --noclean                doesn't empty test files

        EOT;
        echo $usage_msg;
        exit(0);
    }

    public function __toString()
    {
        return "Directory:  $this->directory\n" .
            "Recursive:  $this->recursive\n" .
            "Parse scr:  $this->parse_script\n" .
            "Inter scr:  $this->int_script\n" .
            "Parse only: $this->parse_only\n" .
            "Inter only: $this->int_only\n" .
            "JExamXML:   $this->jexampath\n" .
            "No clean:   $this->no_clean";
    }
}

/* testinfo.php */
?>
