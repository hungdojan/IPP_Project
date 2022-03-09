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

$test_dst = "test_build";
$tp = new TestProcess($test_dst);
$tp->run_test($tp->ti->directory, TestType::BOTH);
$tp->get_results();
if (!$tp->ti->no_clean)
{
    clean_directory($test_dst);
    rmdir($test_dst);
}
/* test.php */
?>
