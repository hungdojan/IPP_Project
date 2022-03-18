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