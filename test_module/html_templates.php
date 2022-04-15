<?php
/**
 * Static class with HTML templates for generating test results
 *
 * This source code serves as submission for
 * second part of the project of class IPP at FIT, BUT 2021/2022
 *
 * @author  Hung Do
 */

class HtmlTemplates
{
    public static $colors = [
        'red'    => 'rgba(232,66,88,1)',
        'orange' => 'rgba(253,128,96,1)',
        'yellow' => 'rgba(254,225,145,1)',
        'green'  => 'rgba(95,167,119,1)'
    ];
    public static function get_body() {
        # workaround to pass this file's dirname into HEREDOC
        $fun_name = 'dirname';
        return <<<EOT
        <!DOCTYPE html>
        <html>
        <head>
            <link rel="stylesheet" href="{$fun_name(__FILE__)}/extra/style.css" />
            <title>IPPcode22 Test Results</title>
        </head>
        <body>
        </body>
        <script src="{$fun_name(__FILE__)}/extra/script.js"></script>
        </html>
        EOT;
    }

    public static $test_passed = <<<EOT
    <div id="test1" class="testPassed">
        <h2></h2>
        <div class="testContent">
            <div class="leftPanel">
                <p></p>
                <p class="log"></p>
            </div>
            <div class="symbol">
                <p class="goodResult">&#x2713;</p>
            </div>
        </div>
    </div>
    EOT;

    public static $test_failed = <<<EOT
    <div class="testFailed">
        <h2></h2>
        <div class="testContent">
            <div class="leftPanel">
                <p></p>
                <p class="log"></p>
            </div>
            <div class="symbol">
                <p class="badResult">&#x2715;</p>
            </div>
        </div>
    </div>
    EOT;

    public static $test_results = <<<EOT
    <div id="testResult">
        <h1>TEST RESULTS</h1>
        <div id="testResultContent">
            <div id="resultLeftPanel">
                <p></p>
            </div>
            <div id="percentage">
                <p id="percentageText"></p>
            </div>
        </div>
        <p id="help">Click on this <b>Test Results</b> window to toggle failed tests filter<br/>
           To get more informations about test unit click on the corresponding test section</p>
    </div>
    EOT;

}
/* html_templates.php */
?>
