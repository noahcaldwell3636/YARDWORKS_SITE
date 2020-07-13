import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'YW_site.settings')

import django
django.setup()

from library.models import Equipment, Usage
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
    print("<><><> POPULATING SERVICES MODEL <><><><")
    print("<><><><><><><><><><><><><><><><><><><><>")

    projpath = os.path.dirname(os.path.abspath(__file__))
    datapath = os.path.join("data","Usage_Since2019.xlsx")
    path = os.path.join(projpath, datapath)

    workbook = xlrd.open_workbook(path)
    worksheet = workbook.sheet_by_index(0)

    for row in range(1, worksheet.nrows):
        # connect to Equipment Model to find ID
        key_var = worksheet.cell_value(row, 0)
        try:  # Cannot retrieve eq_id if no key is provided
            id_var = Equipment.objects.filter(key=key_var).first().ident
        except AttributeError:
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
            print("problem! couldn't find match key")
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
            id_var = "No eq. key provided"

        # Get values and assign to MO objects
        s = Usage.objects.get_or_create(
            key = key_var,
            units = worksheet.cell_value(row, 1),
            date = worksheet.cell_value(row, 3),
            equipment = Equipment.objects.filter(key=key_var).first(),
        )[0]
        s.save()

        # Output to terminal
        print("#######################################")
        print("Adding Usage to " + str(id_var))
        print(str(format_date_windows(worksheet.cell_value(row, 3))) + " " + str(worksheet.cell_value(row, 1)))
        print("#######################################")

    print("<><><><><><><><><><><><><><><><><><><><>")
    print("<><><><><> POPULATION  COMPLETE <><><><>")
    print("<><><><><><><><><><><><><><><><><><><><>")