
function calender() {
    $(".weekly-picker").each(function(index) {
            moment.locale('en', {
            week: { dow: 1 } // Monday is the first day of the week
        });
        //Initialize the datePicker(I have taken format as mm-dd-yyyy, you can     //have your owh)
        $(this).datetimepicker({
            format: 'MM-DD-YYYY'
        });
        //Get the value of Start and End of Week
        $(this).on('dp.change', function (e) {
            var value = $(this).val();
            var firstDate = moment(value, "MM-DD-YYYY").day(1).format("MM-DD-YYYY");
            var lastDate =  moment(value, "MM-DD-YYYY").day(7).format("MM-DD-YYYY");
            $(this).val(firstDate + " - " + lastDate);
        });
    });
}


function addSection() {
    // const csrftoken = Cookies.get('csrftoken');
    var eq_sections = document.getElementsByClassName("add_after_me");
    var last_section = eq_sections[eq_sections.length - 1];
    last_section.insertAdjacentHTML("afterend", last_section.outerHTML);
    disableButton();
    calender()
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
    var form_data = new FormData();
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
        form_data.append("submitter_" + i, submitter.value);
        form_data.append("date_" + i, date.value);
        form_data.append("equipment_" + i, equipment_id.value);
        form_data.append("image_" + i, image.value);
        form_data.append("sub_" + i, submitter.value);
    }
    xhttp.send(form_data);
}









