import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'YW_site.settings')

import django
django.setup()

import csv
from library.models import Equipment

if __name__ == '__main__':
    print("<><><> starting equipment population <><><>")
    csv_data = []
    with open("data/lib.csv") as file:
        reader = csv.reader(file, delimiter=",")
        for row in reader:
            csv_data.append(row)

    titles = [
        "ID",
        "Model",
        "Date Aquired",
        "VIN or SN",
        "License",
        "Ass. Loc",
    ]

    formatted_data = []
    # for item in csv_data:
    #     if item != csv_data[0]:
    #         e = Equipment.objects.get_or_create(
    #             ident=item[0],
    #             model=item[1],
    #             date_aq=item[2],
    #             vin=item[3],
    #             licen=item[4],
    #             ass_loc=item[5],
    #         )[0]
    #         e.save()
    #         print("updating " + str(e) + " to DB")

    print("<><><> population complete <><><>")