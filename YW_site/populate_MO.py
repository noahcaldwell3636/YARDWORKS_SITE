import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'YW_site.settings')

import django
django.setup()

from library.models import MaintenanceOrder
from library.models import Equipment
import os.path
import xlrd

def format_date_windows(days_from_1899):
    """windows OS stores dates as the number of days from 12/31/1899.
    this method will convert the number of days to an actual date."""
    # if the xlsx cell for a date is black it will return an empty string which 
    # will later cause a value error when trying to format. returning an empty 
    # string is suffcient if this is the cause
    try:
        float(days_from_1899)
    except ValueError:
        if days_from_1899 == "":
            return days_from_1899
     # "0" param is for windows config, "1" would be for mac if needed in future
    or_date = xlrd.xldate_as_tuple(float(days_from_1899), 0) 
    # Format: MM/DD/YYYY
    return str(or_date[1]) + "/" + str(or_date[2]) + "/" + str(or_date[0])


if __name__ == "__main__":
    print("<><><><><><><><><><><><><><><><><><><><>")
    print("<> POPULATING MAINTENANCE.ORDER MODEL <>")
    print("<><><><><><><><><><><><><><><><><><><><>")

    projpath = os.path.dirname(os.path.abspath(__file__))
    datapath = os.path.join("data","MaintenanceOrder.xlsx")
    path = os.path.join(projpath, datapath)

    workbook = xlrd.open_workbook(path)
    worksheet = workbook.sheet_by_index(0)

    for row in range(1, worksheet.nrows):
        # connect to Equipment Model to find ID
        key_var = worksheet.cell_value(row, 3)
        num_var = worksheet.cell_value(row, 0)
        try:  # Cannot retrieve eq_id if no key is provided
            id_var = Equipment.objects.filter(key=key_var).first().ident
        except AttributeError:
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
            print("-------------------->Order #" + str(num_var) + " likely doesn't have a eq. key value")
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
            id_var = "No eq. key provided"



        # Get values and assign to MO objects
        mo = MaintenanceOrder.objects.get_or_create(
            num = worksheet.cell_value(row, 0),
            date_ordered = format_date_windows(worksheet.cell_value(row, 1)),
            order_type = worksheet.cell_value(row, 2),
            eq_key = worksheet.cell_value(row, 3),
            eq_id = id_var,
            status = worksheet.cell_value(row, 4),
            comment = worksheet.cell_value(row, 5),
            completed_date = format_date_windows(worksheet.cell_value(row, 6)),
            equipment = Equipment.objects.filter(key=key_var).first()
        )[0]
        mo.save()

        # Output to terminal
        print("#######################################")
        print("num = " + str(worksheet.cell_value(row, 0)))
        print("date_ordered = " + format_date_windows(worksheet.cell_value(row, 1)))
        print("order_type = " + str(worksheet.cell_value(row, 2)))
        print("eq_key = " + str(worksheet.cell_value(row, 3)))
        print("status = " + str(worksheet.cell_value(row, 4)))
        print("comment = " + "(((((" + str(worksheet.cell_value(row, 5)) + "))))))")
        print("completed date = " + format_date_windows(worksheet.cell_value(row, 6)))
        print("#######################################")

    print("<><><><><><><><><><><><><><><><><><><><>")
    print("<><><><><> POPULATION  COMPLETE <><><><>")
    print("<><><><><><><><><><><><><><><><><><><><>")
