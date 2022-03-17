Array.from(document.getElementsByClassName('testPassed')).forEach(elem => {
    elem.onclick = function () {
        if (elem.children[1].style.display === '' || elem.children[1].style.display === 'none') {
            elem.children[1].style.display = 'flex';
        } else {
            elem.children[1].style.display = 'none';
        }
    }
});

Array.from(document.getElementsByClassName('testFailed')).forEach(elem => {
    elem.onclick = function () {
        if (elem.children[1].style.display === '' || elem.children[1].style.display === 'none') {
            elem.children[1].style.display = 'flex';
        } else {
            elem.children[1].style.display = 'none';
        }
    }
});