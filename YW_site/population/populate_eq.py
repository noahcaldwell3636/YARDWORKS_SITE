import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'YW_site.settings')

import django
django.setup()

from library.models import Equipment
import os.path
import xlrd

print("<><><><><><><><><><><><><><><><><><><><>")
print("<><><> POPULATING EQUIPMENT MODEL <><><>")
print("<><><><><><><><><><><><><><><><><><><><>")
# Get data directory location
projpath = os.path.dirname(os.path.abspath(__file__))
datapath = os.path.join("data","Equipment.xlsx")
path = os.path.join(projpath, datapath)
# Create worksheet object for the equipment sheet holding the 
# core attributes
workbook = xlrd.open_workbook(path)
worksheet_core = workbook.sheet_by_index(0)
# Create a service sheet object
datapath2 = os.path.join("data","Service.xlsx")
path = os.path.join(projpath, datapath2)
workbook2 = xlrd.open_workbook(path)
worksheet_service = workbook2.sheet_by_index(0)
# fill values for each piece of equipment
for row in range(1, worksheet_core.nrows):
    if worksheet_core.cell_value(row, 0) == worksheet_service.cell_value(row, 0):
        e = Equipment.objects.get_or_create(
            # Core Fields
            ident = worksheet_core.cell_value(row, 0),
            key = worksheet_core.cell_value(row, 13),
            desc = worksheet_core.cell_value(row, 1),
            interval_unit = worksheet_core.cell_value(row, 2),
            class_code = worksheet_core.cell_value(row, 3),
            location_code = worksheet_core.cell_value(row, 4),
            department_code = worksheet_core.cell_value(row, 5),
            model = worksheet_core.cell_value(row, 6),
            vin = worksheet_core.cell_value(row, 7),
            make = worksheet_core.cell_value(row, 9),
            size = worksheet_core.cell_value(row, 10),
            licen = worksheet_core.cell_value(row, 11),
            year = worksheet_core.cell_value(row, 12),
            # Service Fields
            oil_a = worksheet_service.cell_value(row, 1),
            oil_b = worksheet_service.cell_value(row, 2),
            fuel_a = worksheet_service.cell_value(row, 3),
            fuel_b = worksheet_service.cell_value(row, 4),
            air_in = worksheet_service.cell_value(row, 5),
            air_out = worksheet_service.cell_value(row, 6),
            cab_a = worksheet_service.cell_value(row, 7),
            cab_b = worksheet_service.cell_value(row, 8),
            water_sep = worksheet_service.cell_value(row, 9),
            oil_gal = worksheet_service.cell_value(row, 10),
            main_cost = worksheet_service.cell_value(row, 11),
            current_units = worksheet_service.cell_value(row, 12)
        )[0]    
        e.save()
        # output to temrinal
        print("")
        print(">>>Updating " + str(e) + "<<<")
        print("ident = " + str(worksheet_core.cell_value(row, 0)))
        print("key = " + str(worksheet_core.cell_value(row, 13)))
        print("desc = " + str(worksheet_core.cell_value(row, 1)))
        print("interval_unit = " + str(worksheet_core.cell_value(row, 2)))
        print("class_code = " + str(worksheet_core.cell_value(row, 3)))
        print("location_code = " + str(worksheet_core.cell_value(row, 4)))
        print("department_code = " + str(worksheet_core.cell_value(row, 5)))
        print("model = " + str(worksheet_core.cell_value(row, 6)))
        print("vin = " + str(worksheet_core.cell_value(row, 7)))
        print("make = " + str(worksheet_core.cell_value(row, 9)))
        print("size = " + str(worksheet_core.cell_value(row, 10)))
        print("licen = " + str(worksheet_core.cell_value(row, 11)))
        print("year = " + str(worksheet_core.cell_value(row, 12)))
        print("oil_a = " + str(worksheet_service.cell_value(row, 1)))
        print("oil_b = " + str(worksheet_service.cell_value(row, 2)))
        print("fuel_a = " + str(worksheet_service.cell_value(row, 3)))
        print("fuel_b = " + str(worksheet_service.cell_value(row, 4)))
        print("air_in = " + str(worksheet_service.cell_value(row, 5)))
        print("air_out = " + str(worksheet_service.cell_value(row, 6)))
        print("cab_a = " + str(worksheet_service.cell_value(row, 7)))
        print("cab_b = " + str(worksheet_service.cell_value(row, 8)))
        print("water_sep = " + str(worksheet_service.cell_value(row, 9)))
        print("oil_gal = " + str(worksheet_service.cell_value(row, 10)))
        print("main_cost = " + str(worksheet_service.cell_value(row, 11)))
    else:
        raise IndexError("Equipment ID's did not align for the service and equipment data sheets | "
            + "Eq. sheet ID = " + worksheet_core.cell_value(row, 0) + " | "
            + "Service Sheet ID = " + worksheet_service.cell_value(row, 0))


print("<><><><><><><><><><><><><><><><><><><><>")
print("<><><><><> POPULATION  COMPLETE <><><><>")
print("<><><><><><><><><><><><><><><><><><><><>")
