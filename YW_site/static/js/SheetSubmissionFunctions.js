function addSection() {
    const csrftoken = Cookies.get('csrftoken');
    var eq_sec = document.getElementById("add_after_me");
    eq_sec.insertAdjacentHTML("afterend", eq_sec.outerHTML);
    disableButton()
}

function removeSection(button) {
    const csrftoken = Cookies.get('csrftoken');
    var section_div = button.parentElement
    section_div.parentElement.removeChild(section_div)
    disableButton()
}

function disableButton() {
    const csrftoken = Cookies.get('csrftoken');
    var eq_sections = document.getElementsByClassName("equipment-section")
    buttons = document.getElementsByClassName("remover")
    if (eq_sections.length == 1) {
        buttons[0].disabled = true;
    } else {
        var i;
        for (i = 0; i < buttons.length; i++) {
            buttons[i].disabled = false;
        }
    }
}

function submitForms() {
    for(var i=0, n=document.forms.length; i<n; i++){
        document.forms[i].onsubmit();
    }
}