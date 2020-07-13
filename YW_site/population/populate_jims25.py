""" The purpose of this script is to create a sales report in
CSV format given a list of customers and time division.
"""
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'YW_site.settings')

from django import setup
setup()

import os.path 
from app_reports.models import CompanyGroup
from app_reports.models import Company
from app_reports.models import MonthlySalesTotal
import xlrd, csv



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
    date = xlrd.xldate_as_tuple(float(days_from_1899), 0) 
    # Format: MM/DD/YYYY
    return str(date[1]) + "/" + str(date[2]) + "/" + str(date[0])



if __name__ == "__main__":
    # Get Data Directory path
    projpath = os.path.dirname(os.path.abspath(__file__))
    datapath = os.path.join("data","JimHallsReport.xlsx")
    path = os.path.join(projpath, datapath)
    # retrieve excel data
    wb = xlrd.open_workbook(path)
    sheet_25 = wb.sheet_by_name('25_Customers')
    sheet_inv = wb.sheet_by_name("Invoices_Master")

    jims25 = {}
    for row in range(1, sheet_25.nrows):
        account = str(sheet_25.cell(row,0)).replace("'", "").replace("number:", "")
        account = str(int(float(account)))
        account = "0"*(7 - len(account)) + account

        company = str(sheet_25.cell(row,1)).replace("'", "").replace("text:", "").replace('"', "")

        jims25[account] = {
            'account': account,
            'company': company,
            '2014': {'1':0.0, '2':0.0, '3':0.0, '4':0.0, '5':0.0, '6':0.0, '7':0.0, '8':0.0, '9':0.0, '10':0.0, '11':0.0, '12':0.0},
            '2015': {'1':0.0, '2':0.0, '3':0.0, '4':0.0, '5':0.0, '6':0.0, '7':0.0, '8':0.0, '9':0.0, '10':0.0, '11':0.0, '12':0.0},
            '2016': {'1':0.0, '2':0.0, '3':0.0, '4':0.0, '5':0.0, '6':0.0, '7':0.0, '8':0.0, '9':0.0, '10':0.0, '11':0.0, '12':0.0},
            '2017': {'1':0.0, '2':0.0, '3':0.0, '4':0.0, '5':0.0, '6':0.0, '7':0.0, '8':0.0, '9':0.0, '10':0.0, '11':0.0, '12':0.0},
            '2018': {'1':0.0, '2':0.0, '3':0.0, '4':0.0, '5':0.0, '6':0.0, '7':0.0, '8':0.0, '9':0.0, '10':0.0, '11':0.0, '12':0.0},
            '2019': {'1':0.0, '2':0.0, '3':0.0, '4':0.0, '5':0.0, '6':0.0, '7':0.0, '8':0.0, '9':0.0, '10':0.0, '11':0.0, '12':0.0},
            '2020': {'1':0.0, '2':0.0, '3':0.0, '4':0.0, '5':0.0, '6':0.0, '7':0.0, '8':0.0, '9':0.0, '10':0.0, '11':0.0, '12':0.0}
        }

    for row in range(1, sheet_inv.nrows):
        account = str(sheet_inv.cell(row,0)).replace("'", "").replace("text:", "")
        try:
            account = str(int(float(account)))
        except:
            account = "0000000"
        account = "0"*(7 - len(account)) + account


        if account in jims25:
            date = str(sheet_inv.cell(row, 2)).replace("xldate:", "")
            date = format_date_windows(date)
            month = int(date.split("/")[0])
            day = int(date.split("/")[1])
            year = int(date.split("/")[2])

            nontax = float(str(sheet_inv.cell(row, 7)).replace("number:", ""))
            taxable = float(str(sheet_inv.cell(row, 8)).replace("number:", ""))

            jims25[account][str(year)][str(month)]  += round((nontax + taxable), 2)

    group = CompanyGroup.objects.filter(name="JimsCustomers").first()

    for acc in jims25:

        company = Company.objects.get_or_create(
            name = jims25[acc]['company'],
            account = jims25[acc]['account'],
        )[0]

        company.groups.add(group)

        # 2014 -----------------------------------
        for mst in jims25[acc]['2014'].items():
           mst_2014 = MonthlySalesTotal.objects.get_or_create(
                company = company,
                month = mst[0],
                year = 2014,
                amount  = mst[1]
            )[0]

        # 2015 -----------------------------------
        for mst in jims25[acc]['2015'].items():
            mst_2015 = MonthlySalesTotal.objects.get_or_create(
                company = company,
                month = mst[0],
                year = 2015,
                amount  = mst[1]
            )[0]

        # 2016 -----------------------------------
        for mst in jims25[acc]['2016'].items():
            mst_object = MonthlySalesTotal.objects.get_or_create(
                company = company,
                month = mst[0],
                year = 2016,
                amount  = mst[1]
            )[0]

        # 2017 -----------------------------------
        for mst in jims25[acc]['2017'].items():
            mst_object = MonthlySalesTotal.objects.get_or_create(
                company = company,
                month = mst[0],
                year = 2017,
                amount  = mst[1]
            )[0]

        # 2018 -----------------------------------
        for mst in jims25[acc]['2018'].items():
            mst_object = MonthlySalesTotal.objects.get_or_create(
                company = company,
                month = mst[0],
                year = 2018,
                amount  = mst[1]
            )[0]

        # 2019 -----------------------------------
        for mst in jims25[acc]['2019'].items():
            mst_object = MonthlySalesTotal.objects.get_or_create(
                company = company,
                month = mst[0],
                year = 2019,
                amount  = mst[1]
            )[0]

        # 2020 -----------------------------------
        for mst in jims25[acc]['2020'].items():
            mst_object = MonthlySalesTotal.objects.get_or_create(
                company = company,
                month = mst[0],
                year = 2020,
                amount  = mst[1]
            )[0]



