$.ajaxSetup({ 
    beforeSend: function(xhr, settings) {
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        alert('good!')
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    } else {
                        alert("Bad!")
                    }
                }
            }
            return cookieValue;
        }
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
        // Only send the token to relative URLs i.e. locally.
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    } 
});





function addSection() {
    // const csrftoken = Cookies.get('csrftoken');
    var eq_sec = document.getElementById("add_after_me");
    eq_sec.insertAdjacentHTML("afterend", eq_sec.outerHTML);
    disableButton();
}

function removeSection(button) {
    // const csrftoken = Cookies.get('csrftoken');
    var section_div = button.parentElement.parentElement;
    section_div.parentElement.removeChild(section_div);
    disableButton();
}

function disableButton() {
    // const csrftoken = Cookies.get('csrftoken');
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
    var xhttp = new XMLHttpRequest();
    for(var i=0, n=document.forms.length; i<n; i++){
        form = document.forms[i];
        form_els = document.forms[i].elements;
        var csrf = form_els[0];
        var submitter = form_els[1];
        var date = form_els[2];
        var equipment_id = form_els[3];
        var image = form_els[4];
        var url = window.location.href;
        

        xhttp.open("POST", url, true);
        xhttp.setRequestHeader('X-CSRFToken', csrf.value); 
        var form_data = new FormData();
        form_data.append("submitter", submitter.value);
        form_data.append("date", date.value);
        form_data.append("equipment", equipment_id.value);
        form_data.append("image", image.value);
        form_data.append("sub", submitter.value);
        xhttp.send(form_data);
    }
}

function unhideSheetSubmission() {
    hidden_elements = document.getElementsByClassName("sheet-form")
    for (var i = 0; i < hidden_elements.length; i++) {
        hidden_elements[i].style.visibility = "visible";
    }
}

function hideSheetSubmission() {
    alert('Yo!')
    hidden_elements = document.getElementsByClassName("sheet-form")
    for (var i = 0; i < hidden_elements.length; i++) {
        alert("hit loop!")
        hidden_elements[i].style.visibility = "hidden";
    }
}









