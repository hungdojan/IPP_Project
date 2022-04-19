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
    public static $body = <<<EOT
    <!DOCTYPE html>
    <html>
    <head>
        <style>
        body {
            font-family: 'Roboto', sans-serif;
            font-size: large;
            color: #323232;
        }

        a {
            color: white;
        }

        h1 {
            text-align: center;
            margin: 0%;
            margin-top: 5px;
        }
        h2 {
            text-align: center;
            margin-bottom: 0%;
            margin-top: 3px;
        }


        .testPassed {
            color: white;
            background-color: #5fa777;
            /* background-color: #b0d8a4; */
            margin: 5px;
            margin-left: 5em;
            margin-right: 5em;
        }

        .testFailed {
            color: white;
            /* background-color: #ff6962; */
            background-color: #e84258;
            margin: 5px;
            margin-left: 5em;
            margin-right: 5em;
        }

        .testContent {
            display: none;
            justify-content: center;
            align-items: center;
        }

        .goodResult {
            font-size: 80px;
            text-align: center;
            margin-top: 0%;
            margin-bottom: 0%;
            padding-top: 0%;
            padding-bottom: 0%;
        }

        .badResult {
            font-size: 80px;
            text-align: center;
            margin-top: 0%;
            margin-bottom: 0%;
        }

        #testResult {
            border-style: solid;
            border-color: black;
            border-width: 3px;
            border-radius: 30px;
            margin-left: 20%;
            margin-right: 20%;
        }

        #resultLeftPanel {
            width: 50%;
            font-size: 26px;
            margin: 0%;
        }

        #testResultContent {
            display: flex;
            justify-content: center;
            align-items: center;
        }

        #help {
            text-align: center;
        }

        #percentage {
            font-size: 80px;
            text-align: center;
            margin-top: 0%;
            margin-bottom: 0%;
        }

        #percentageText {
            width:225px;
            margin: 0%;
        }

        .leftPanel {
            width: 70%;
            font-size: larger;
        }

        .log {
            font-family: Lucida Sans Typewriter,Lucida Console,monaco,Bitstream Vera Sans Mono,monospace;
            font-size: 12px;
        }
        </style>
        <title>IPPcode22 Test Results</title>
    </head>
    <body>
    </body>
    </html>
    EOT;

    public static $script = <<<EOT
    <script>
    // expand success test unit
    var testPassedDivs = document.getElementsByClassName('testPassed')
    Array.from(testPassedDivs).forEach(elem => {
        elem.onclick = function () {
            if (elem.children[1].style.display === '' || elem.children[1].style.display === 'none') {
                elem.children[1].style.display = 'flex';
            } else {
                elem.children[1].style.display = 'none';
            }
        }
    });

    // expand failed test unit
    var testFailedDivs = document.getElementsByClassName('testFailed');
    Array.from(testFailedDivs).forEach(elem => {
        elem.onclick = function () {
            if (elem.children[1].style.display === '' || elem.children[1].style.display === 'none') {
                elem.children[1].style.display = 'flex';
            } else {
                elem.children[1].style.display = 'none';
            }
        }
    });

    // show all or show failed tests
    var elem = document.getElementById('testResult');
    var showAll = true;
    elem.onclick = function() {
        if (showAll) {
            Array.from(testPassedDivs).forEach(elem => {
                elem.style.display = 'none';
            });
        } else {
            Array.from(testPassedDivs).forEach(elem => {
                elem.style.display = "";
            });
        }
        showAll = !showAll;
    };
    </script>
    EOT;

    public static $test_passed = <<<EOT
    <div class="testPassed">
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
