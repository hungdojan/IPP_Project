<?php
/**
 * File with test methods
 *
 * This source code serves as submission for
 * second part of the project of class IPP at FIT, BUT 2021/2022
 *
 * @author  Hung Do
 */

require_once "testinfo.php";
require_once "testinstance.php";
require_once "html_generator.php";

class TestProcess
{
    public $output_dir;
    public $output_file;
    public $ti;
    public $lof_tests;

    /**
     * Class constructor
     *
     * @param output_dir    Path to directory to create test outputs
     * @param output_file   Name of final output file
     */
    public function __construct($output_dir='test_build', $output_file='test_out')
    {
        $this->output_dir = $output_dir;
        $this->output_file = $output_file;
        $this->ti = new TestInfo($output_dir);
        $this->lof_tests = [];
    }

    /**
     * Create list of useful file paths for single test
     * Return array with 5 elements
     *      Key         Value
     *      filename    base name
     *      test_dir    path to test unit directory
     *      src         path to '*.src' file
     *      in          path to '*.in' file
     *      out         path to '*.out' file
     *      rc          path to '*.rc' file
     *      log         path to test log file
     *
     * When .rc or .in files don't exist 
     * function creates then with default values (empty .in; 0 in .rc)
     *
     * @param filename Path to '.src' path name
     * @return Array of useful file paths
     */
    private function generate_test_filepaths($filename, $parent_dir)
    {
        $file_pi = pathinfo($filename);
        $files = [
            'filename' => $file_pi['filename'],
            'test_dir' => "$this->output_dir/$file_pi[filename]",
            'testname' => "$parent_dir - $file_pi[filename]",
            'src'      => "$file_pi[dirname]/$file_pi[filename].src",
            'in'       => "$file_pi[dirname]/$file_pi[filename].in",
            'out'      => "$file_pi[dirname]/$file_pi[filename].out",
            'rc'       => "$file_pi[dirname]/$file_pi[filename].rc",
            'log'      => "$this->output_dir/$file_pi[filename]/output.log"
        ];

        // create .rc file
        if (!file_exists($files['rc']))
        {
            $f = fopen($files['rc'], "w");
            fwrite($f, '0');
            fclose($f);
        }
        // create .in file
        if (!file_exists($files['in']))
            shell_exec("touch $files[in]");

        // create .out file
        if (!file_exists($files['out']))
            shell_exec("touch $files[out]");
        return $files;
    }

    /**
     * Remove files and directories created by test session
     *
     * @param Path to test output directory
     */
    private function clean_up($output_dir)
    {
        // clean-up
        $tmp_files = glob("$output_dir/*");
        foreach ($tmp_files as $tf)
            unlink($tf);
    }

    /**
     * Compare return code of executed test with expected value
     * Test ends when return codes don't match or
     * return code's value is not 0.
     * When test passes nof_passed is increased.
     *
     * @param rc      Return code of executed test
     * @param exp_rc  Expected return code
     * @return 'true' when test session ends 
     */
    private function compare_rc($rc, $exp_rc, $t_ins)
    {
        // echo_log("Return code test: ", $logfile);
        // if ($rc != $exp_rc)
        // {
        //     echo_log("FAILED\nExpected $exp_rc, received $rc\n", $logfile);
        //     echo_log("===============================\n\n", $logfile);
        //     return true;
        // }
        // echo_log("OK\n", $logfile);
        // if ($rc != 0)
        // {
        //     $this->ti->nof_passed++;
        //     echo_log("===============================\n\n", $logfile);
        //     return true;
        // }
        // return false;
        $t_ins->ret_code = $rc;
        $t_ins->exp_ret_code = $exp_rc;
        if ($rc != $exp_rc)
        {
            $t_ins->add_rc_log("Expected $exp_rc, received $rc\n");
            return true;
        }
        if ($rc != 0)
        {
            $this->ti->nof_passed++;
            return true;
        }
        $t_ins->add_rc_log("\n");
        return false;
    }

    /**
     * Compare XML output from parse.php with expected XML
     * Uses JExamXML framework to run test
     * When test passes nof_passed is increased
     *
     * @param exp_output_path Path to expected test's output
     */
    private function compare_xml($exp_output_path, $output_path, TestInstance $t_ins)
    {
        $exec_cmd = "java -jar {$this->ti->jexampath}jexamxml.jar $output_path/$this->output_file " .
            "$exp_output_path $output_path/diff.err {$this->ti->jexampath}options 2>/dev/null";

        $t_ins->add_output_log("$exec_cmd\n");

        exec($exec_cmd, $output, $rc);
        $result = count($output) > 2 && $output[2] == "Two files are identical";
        if ($result)
            $this->ti->nof_passed++;

        $t_ins->add_output_log($output);
        $t_ins->add_output_log("\n");
        return $result;
    }

    /**
     * Compare output files with 'diff' command
     * When test passes nof_passed counter is increased
     *
     * @param output_path Path to output file created by test
     * @param exp_output_path Path to expected test's output
     */
    private function compare_diff($output_path, $exp_output_path, $t_ins)
    {
        // echo_log("Output comparison test: ", $logfile);
        // if (!is_file($exp_output_path))
        // {
        //     $this->ti->nof_passed++;
        //     echo_log("OK\n", $logfile);
        //     echo_log("===============================\n\n", $logfile);
        //     return;
        // }
        $exec_cmd = "diff $output_path $exp_output_path";
        $t_ins->add_output_log("$exec_cmd\n");
        exec($exec_cmd, $diff, $rc);

        // if output of 'diff' program is empty
        // both output files are identical
        if (!$diff)
            $this->ti->nof_passed++;

        $t_ins->add_output_log($diff);
        $t_ins->add_output_log("\n");
        return !$diff;
    }

    /**
     * Run all test in given directory
     * When $ti->recursive flag is toggled, tests are also run in subdirectories
     *
     * @param src_dir Source directory
     * @param test_type Type of test (enum TestType)
     */
    public function run_test($src_dir)
    {
        // append '/' to directory path if needed
        if (!preg_match('/\/$/', $src_dir))
            $src_dir .= '/';

        // scan current directory
        $dirs = glob("$src_dir*", GLOB_ONLYDIR);
        $test_files = glob("$src_dir*.src");

        // recursive subdirectories scan
        if (count($dirs) > 0 && $this->ti->recursive)
        {
            foreach ($dirs as $dir)
                $this->run_test($dir);
        }

        // no test files found
        if (count($test_files) < 1)
            return;
        

        if ($this->ti->parse_only)
            $this->parse_only($src_dir, $test_files);
        elseif ($this->ti->int_only)
            $this->int_only($src_dir, $test_files);
        else
            $this->both($src_dir, $test_files);
    }

    /**
     * Print results
     */
    public function get_results()
    {
        echo "Test results: {$this->ti->nof_passed}/{$this->ti->nof_tests}\n";
    }

    private function parse_only($test_name, $test_files)
    {
        foreach ($test_files as $file)
        {
            $this->ti->nof_tests++;
            $files = $this->generate_test_filepaths($file, $test_name);
            $t_ins = new TestInstance($files['testname']);
            if (!is_dir($files['test_dir']))
                mkdir($files['test_dir']);

            $exec_cmd = TestInfo::PHP_EXEC." {$this->ti->parse_script} < $files[src]".
                " > $files[test_dir]/$this->output_file 2> $files[log]";
            
            $t_ins->add_rc_log($exec_cmd."\n");

            // executing test
            exec($exec_cmd, $output, $rc);
            $exp_rc = file_get_contents($files['rc']);
            $t_ins->add_rc_log(file_get_contents($files['log']));

            // compare return codes
            // if function returns false (meaning test is not done yet)
            // program compares xml outputs
            if (!$this->compare_rc($rc, $exp_rc, $t_ins))
                $t_ins->output_result = $this->compare_xml($files['out'], $files['test_dir'], $t_ins);

            // clean-up created test files
            // when --noclean flag is used, program leaves files as they are
            // and stores its path name in $t_ins->output_file
            if (!$this->ti->no_clean)
            {
                $this->clean_up($files['test_dir']);
                rmdir($files['test_dir']);
            }
            else
            {
                $t_ins->output_file = realpath("$files[test_dir]/$this->output_file");
            }
            // append test instance into list of tests for later HTML display
            array_push($this->lof_tests, $t_ins);
            echo "$files[testname] done\n";
        }
    }

    private function int_only($test_name, $test_files)
    {
        foreach ($test_files as $file)
        {
            $this->ti->nof_tests++;
            $files = $this->generate_test_filepaths($file, $test_name);
            $t_ins = new TestInstance($files['testname']);
            if (!is_dir($files['test_dir']))
                mkdir($files['test_dir']);

            // test name
            $exec_cmd = TestInfo::PY_EXEC." {$this->ti->int_script} --source $files[src]".
                " --input $files[in] > $files[test_dir]/$this->output_file 2> $files[log]";

            $t_ins->add_rc_log($exec_cmd."\n");

            // return code test
            exec($exec_cmd, $output, $rc);
            $exp_rc = file_get_contents($files['rc']);
            $t_ins->add_rc_log(file_get_contents($files['log']));
            if (!$this->compare_rc($rc, $exp_rc, $t_ins))
                $t_ins->output_result = $this->compare_diff("$files[test_dir]/$this->output_file",
                                                            $files['out'], $t_ins);

            if (!$this->ti->no_clean)
            {
                $this->clean_up($files['test_dir']);
                rmdir($files['test_dir']);
            }
            else
            {
                $t_ins->output_file = realpath("$files[test_dir]/$this->output_file");
            }
            array_push($this->lof_tests, $t_ins);
            echo "$files[testname] done\n";
        }
    }

    private function both($test_name, $test_files)
    {
        foreach ($test_files as $file)
        {
            $this->ti->nof_tests++;
            $files = $this->generate_test_filepaths($file, $test_name);
            $t_ins = new TestInstance($files['testname']);
            if (!is_dir($files['test_dir']))
                mkdir($files['test_dir']);

            // test name
            $exec_cmd = TestInfo::PHP_EXEC." {$this->ti->parse_script} < $files[src] | ".
                TestInfo::PY_EXEC." {$this->ti->int_script} --input $files[in] > ". 
                "$files[test_dir]/$this->output_file 2>> $files[log]";

            $t_ins->add_rc_log($exec_cmd."\n");

            // return code test
            exec($exec_cmd, $output, $rc);
            $exp_rc = file_get_contents($files['rc']);
            $t_ins->add_rc_log(file_get_contents($files['log']));
            if (!$this->compare_rc($rc, $exp_rc, $t_ins))
                $t_ins->output_result = $this->compare_diff("$files[test_dir]/$this->output_file",
                                                            $files['out'], $t_ins);
            if (!$this->ti->no_clean)
            {
                $this->clean_up($files['test_dir']);
                rmdir($files['test_dir']);
            }
            else
            {
                $t_ins->output_file = realpath("$files[test_dir]/$this->output_file");
            }
            array_push($this->lof_tests, $t_ins);
            echo "$files[testname] done\n";
        }
    }

    public function generate_html()
    {
        $hg = HtmlGenerator::get_instance();
        $hg->generate_results($this->ti->nof_passed, $this->ti->nof_tests);
        foreach ($this->lof_tests as $test_instance)
            $hg->add_test_instance($test_instance);
        $hg->generate_files('index.html');
    }

}
/* testinfo.php */
