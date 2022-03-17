<?php

class HtmlTemplates
{
    public static $colors = [
        'red'    => 'rgba(232,66,88,1)',
        'orange' => 'rgba(253,128,96,1)',
        'yellow' => 'rgba(254,225,145,1)',
        'green'  => 'rgba(95,167,119,1)'
    ];
    public static $body = <<<EOT
    <!DOCTYPE html>
    <html>
    <head>
        <link rel="stylesheet" href="test_module/extra/style.css" />
        <title>IPPcode22 Test Results</title>
    </head>
    <body>
    </body>
    <script src="test_module/extra/script.js"></script>
    </html>
    EOT;

    public static $test_passed = <<<EOT
    <div id="test1" class="testPassed">
        <h2></h2>
        <div class="testContent">
            <div class="leftPanel">
                <p></p>
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
    </div>
    EOT;

    public static $style_css = <<<EOT
    EOT;

    public static $script_js = <<<EOT
    EOT;
}
?>
