import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'YW_site.settings')

import django
django.setup()

from app_library.models import Equipment, Services
import os.path
import xlrd

if __name__ == "__main__":
    print("<><><><><><><><><><><><><><><><><><><><>")
    print("<><><> POPULATING SERVICES MODEL <><><><")
    print("<><><><><><><><><><><><><><><><><><><><>")

    projpath = os.path.dirname(os.path.abspath(__file__))
    datapath = os.path.join("data","OILCHANGES_SINCE2019.xlsx")
    path = os.path.join(projpath, datapath)

    workbook = xlrd.open_workbook(path)
    worksheet = workbook.sheet_by_index(0)

    for row in range(1, worksheet.nrows):
        # connect to Equipment Model to find ID
        key_var = worksheet.cell_value(row, 1)
        try:  # Cannot retrieve eq_id if no key is provided
            id_var = Equipment.objects.filter(key=key_var).first().ident
        except AttributeError:
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
            print("problem! couldn't find match key")
            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
            id_var = "No eq. key provided"

        num_var = worksheet.cell_value(row, 0)



        # Get values and assign to MO objects
        s = Services.objects.get_or_create(
            key = key_var,
            equipment = Equipment.objects.filter(key=key_var).first(),
            num = worksheet.cell_value(row, 0)
        )[0]
        s.save()

        # Output to terminal
        print("#######################################")
        print("Adding Service #" + worksheet.cell_value(row, 0) + " to " + str(id_var) )
        print("#######################################")

    print("<><><><><><><><><><><><><><><><><><><><>")
    print("<><><><><> POPULATION  COMPLETE <><><><>")
    print("<><><><><><><><><><><><><><><><><><><><>")