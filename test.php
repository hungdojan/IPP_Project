<?php
/**
 * Main script
 *
 * This source code serves as submission for
 * second part of the project of class IPP at FIT, BUT 2021/2022
 *
 * @author  Hung Do
 */

require_once "test_module/testinfo.php";
require_once "test_module/testprocess.php";

// test initialization
$test_dst = "test_build";
$tp = new TestProcess($test_dst);

// test execution
$tp->run_test($tp->ti->directory);
$tp->get_results();
$tp->generate_html();

// clean up created test directory
if (!$tp->ti->no_clean)
{
    remove_test_directory($test_dst);
    rmdir($test_dst);
}
/* test.php */
?>
