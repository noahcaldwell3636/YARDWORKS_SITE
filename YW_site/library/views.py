from django.shortcuts import render
from django.urls import path
from library.models import Equipment
from django.views.decorators.csrf import csrf_protect
from . import forms

# Default Table View
def render_table(request):
    eq_list = Equipment.objects.order_by('ident')
    eq_dict = {'eq_list': eq_list}
    return render(request, "library.html", context=eq_dict)

# Table View By ID
def render_table_byid(request):
    eq_list = Equipment.objects.order_by('ident')
    eq_dict = {'eq_list': eq_list}
    return render(request, "library.html", context=eq_dict)

# Table View By Location
def render_table_byloc(request):
    eq_list = Equipment.objects.order_by('location_code')
    eq_dict = {'eq_list': eq_list}
    return render(request, "library.html", context=eq_dict)

# Table View By Location
def render_table_bymake(request):
    eq_list = Equipment.objects.order_by('make')
    eq_dict = {'eq_list': eq_list}
    return render(request, "library.html", context=eq_dict)

##################################################################
##################################################################

# Individual Equipment View
def render_indiv_eq(request):
    # Get the ID of the eq. that the user selected from the table,
    # communicated through the URL
    name = request.get_full_path().split("/")[-1]
    # declare eq. variables for html reference
    eq_dict = get_current_next_prev(name)
    current = eq_dict["current"]
    next = eq_dict["next"]
    prev = eq_dict["prev"]
    # get the first and last vehicles on the list
    start = Equipment.objects.order_by('ident').first()
    end = Equipment.objects.order_by('ident').last()
    # get maintenance order list
    morders = current.maintenanceorder_set.all()
    # get invoice list
    invoices = current.equipmentinvoice_set.all()
    # get invoice total
    inv_total = 0
    for inv in invoices:
        inv_total += float(inv.amount)
    inv_total = "{:,}".format(round(inv_total, 2))
    # get service count since 2019
    serv_since2019 = current.services_set.all()
    serv_count = serv_since2019.count()
    if current.main_cost == '':
        serv_cost = float(serv_count) * 0
    else:
        serv_cost = float(serv_count) * float(current.main_cost.replace("$","").replace(" + oil", ""))
    serv_cost = round(serv_cost, 2)

    # get hours since 1/1/2019
    usage = current.usage_set.all()
    low = 9999999 # bad practice
    for u in usage:
        if int(u.units) < int(low):
            low = u.units
    if low == 9999999:
        low = "bad or non-existant usage data"
    # Get Usage from 2019 till now if data is good
    if current.current_units == '' or low == '' or low == "bad or non-existant usage data":
        usage = "bad usage data"
    else:
        usage = float(current.current_units) - float(low) 
    # render html and provide it variable calculated above
    return render(request, "indiv_eq.html", context={"eq": current,
                                                    "prev":prev, 
                                                    "next":next,
                                                    "start":start,
                                                    "end":end,
                                                    "morders":morders,
                                                    "invoices":invoices,
                                                    "inv_total":inv_total,
                                                    "serv_since2019":serv_since2019,
                                                    "serv_count":serv_count,
                                                    "serv_cost":serv_cost,
                                                    "begin_units":low,
                                                    "usage":usage,
                                                    })

##################################################################
#################  EQUIPMENT SHEETS  #############################
##################################################################

def render_eq_sheet_table(request):
    eq_list = Equipment.objects.order_by('ident')
    eq_dict = {'eq_list': eq_list}
    return render(request, 'eq_sheet_table.html', context=eq_dict)

@csrf_protect
def render_sheet_submission(request):
    print("()()()()()()()()()()")

    group_form = forms.EquipmentSheetGroup()
    sheet_form = forms.EquipmentSheetForm()

    if request.method == "POST":
        form_submission = forms.EquipmentSheetGroup(request.POST)
        print("post?")
        if form_submission.is_valid():
            print("validation succussful!")
            print(form_submission.cleaned_data)
        else:
            print(form_submission.errors)
    else:
        print("ran, but not post malone")

    return render(request, 'sheet_submission_form.html', {
        'group_form':group_form,
        'sheet_form':sheet_form
    })


##################################################################
#################  HELPER METHODS  ###############################
##################################################################


def get_current_next_prev(identity):
    """Retrieves the equipment with the a specified ID as well 
    as the previous and next equipments in the form of a list.
    _____params______ 
    >>> str: The identity of the current equipment you want to view
    _____returns______
    >>> list: [current , next, previous]
    """
    # Declare result vars
    current = next = prev = None
    # eq list to pull info from
    # TODO: make eq_list the same list that the user defined
    # on the previous page with proper filters and sorting
    eq_list = Equipment.objects.order_by('ident')
    # Get Current, Next, and Previous vehicles
    for i in range(len(eq_list)):
        if eq_list[i].ident == identity:
            # get current equipment to display its info
            current = eq_list[i]
            # get prev equiptment on list for paging button
            if i != 0:
                prev = eq_list[i-1]
            else: # prev page return current eq. if on first page
                prev = current 
            # get next equiptment on list for paging button
            if i != len(eq_list)-1:
                next = eq_list[i+1]
            else: # next page returns current eq. if on last page
                next = current
    return {"current":current, "next":next, "prev":prev}
