""" This Script is meant to populate the all the invoice objects from the 
invoices.xlsx file in the data folder.
"""
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'YW_site.settings')

from django import setup
setup()

import os.path 
from reports.models import Company, Invoice
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
        if days_from_1899 == "" or days_from_1899 == "empty:":
            return None
     # "0" param is for windows config, "1" would be for mac if needed in future
    date = xlrd.xldate_as_tuple(float(days_from_1899), 0) 
    # Format: MM/DD/YYYY
    return "0"*(4-len(str(date[0])))+str(date[0]) + "-" + "0"*(2-len(str(date[1])))+str(date[1]) + "-" + "0"*(2-len(str(date[2])))+str(date[2])


if __name__ == "__main__":
    # Get Data Directory path
    projpath = os.path.dirname(os.path.abspath(__file__))
    datapath = os.path.join("data","invoices.xlsx")
    path = os.path.join(projpath, datapath)
    # retrieve excel data
    wb = xlrd.open_workbook(path)
    sheet_inv = wb.sheet_by_name("Invoice_Data")
    print(sheet_inv)
    # create a dictionary of dictionaries of each invoice
    invoices = {}
    count = 1
    for row in range(1, sheet_inv.nrows):
        number = str(sheet_inv.cell(row,0)).replace("'", "").replace("text:", "")
        date = format_date_windows(str(sheet_inv.cell(row,1)).replace("'", "").replace("xldate:", ""))
        customer_number = str(sheet_inv.cell(row,2)).replace("'", "").replace("text:", "")
        sale_type = str(sheet_inv.cell(row,3)).replace("'", "").replace("text:", "")
        bill_to_name = str(sheet_inv.cell(row,4)).replace("'", "").replace("text:", "")
        bill_to_address = str(sheet_inv.cell(row,5)).replace("'", "").replace("text:", "")
        bill_to_city = str(sheet_inv.cell(row,6)).replace("'", "").replace("text:", "")
        bill_to_state = str(sheet_inv.cell(row,7)).replace("'", "").replace("text:", "")
        bill_to_zip = str(sheet_inv.cell(row,8)).replace("'", "").replace("text:", "")
        ship_to_name = str(sheet_inv.cell(row,9)).replace("'", "").replace("text:", "")
        ship_to_address = str(sheet_inv.cell(row,10)).replace("'", "").replace("text:", "")
        ship_to_city = str(sheet_inv.cell(row,11)).replace("'", "").replace("text:", "")
        ship_to_state = str(sheet_inv.cell(row,12)).replace("'", "").replace("text:", "")
        ship_to_zip = str(sheet_inv.cell(row,13)).replace("'", "").replace("text:", "")
        ship_date = format_date_windows(str(sheet_inv.cell(row,14)).replace("'", "").replace("xldate:", ""))
        payment_type = str(sheet_inv.cell(row,15)).replace("'", "").replace("text:", "")
        warehouse_code = str(sheet_inv.cell(row,16)).replace("'", "").replace("text:", "")
        taxable_amount = str(sheet_inv.cell(row,17)).replace("'", "").replace("number:", "")
        nontaxable_amount = str(sheet_inv.cell(row,18)).replace("'", "").replace("number:", "")
        freight_amount = str(sheet_inv.cell(row,19)).replace("'", "").replace("number:", "")
        sales_tax_amount = str(sheet_inv.cell(row,20)).replace("'", "").replace("number:", "")
        cost_of_sales = str(sheet_inv.cell(row,21)).replace("'", "").replace("number:", "")
        batch = str(sheet_inv.cell(row,22)).replace("'", "").replace("text:", "")
        
        amount_without_tax = float(taxable_amount) + float(nontaxable_amount) + float(freight_amount)
        amount_with_tax = amount_without_tax + float(sales_tax_amount)
        profit = amount_without_tax - float(cost_of_sales)

        try:
            company = Company.objects.get(account=customer_number)
        except:
            company = Company.objects.create(name=bill_to_name, account=customer_number)

        invoices[number] = {
            'number': number,
            'date': date,
            'customer_number': customer_number,
            'sale_type': sale_type,
            'bill_to_name': bill_to_name,
            'bill_to_address': bill_to_address,
            'bill_to_city': bill_to_city,
            'bill_to_state': bill_to_state,
            'bill_to_zip': bill_to_zip,
            'ship_to_name': ship_to_name,
            'ship_to_address': ship_to_address,
            'ship_to_city': ship_to_city,
            'ship_to_state': ship_to_state,
            'ship_to_zip': ship_to_zip,
            'ship_date': ship_date,
            'payment_type': payment_type,
            'warehouse_code': warehouse_code,
            'taxable_amount': taxable_amount,
            'nontaxable_amount': nontaxable_amount,
            'freight_amount': freight_amount,
            'sales_tax_amount': sales_tax_amount,
            'cost_of_sales': cost_of_sales,
            'batch': batch,
            'amount_without_tax': amount_without_tax,
            'amount_with_tax': amount_with_tax,
            'profit': profit,
            'company': company,
        }

        try:
            Invoice.objects.get(number=number)
            count += 1
            print("")
            print("processing count = " + str(count))
            print("Invoice #" + number)
            print("...invoice already created, retrieved")
        except:
            print("")
            print("processing count = " + str(count))
            print("Invoice #" + number)
            print("...invoice not found creating.......")
            count += 1
            Invoice.objects.create(
                number = number,
                date = date,
                customer_number = customer_number,
                sale_type = sale_type,
                bill_to_name = bill_to_name,
                bill_to_address = bill_to_address,
                bill_to_city = bill_to_city,
                bill_to_state = bill_to_state,
                bill_to_zip = bill_to_zip,
                ship_to_name = ship_to_name,
                ship_to_address = ship_to_address,
                ship_to_city = ship_to_city,
                ship_to_state = ship_to_state,
                ship_to_zip = ship_to_zip,
                ship_date = ship_date,
                payment_type = payment_type,
                warehouse_code = warehouse_code,
                taxable_amount = taxable_amount,
                nontaxable_amount = nontaxable_amount,
                freight_amount = freight_amount,
                sales_tax_amount = sales_tax_amount,
                cost_of_sales = cost_of_sales,
                batch = batch,
                amount_without_tax = amount_without_tax,
                amount_with_tax = amount_with_tax,
                profit = profit,
                company = company,
            )

    print(Invoice.objects.all())


    

        
        













