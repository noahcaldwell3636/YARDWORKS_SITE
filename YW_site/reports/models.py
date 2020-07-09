from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=72)
    account = models.CharField(max_length=72)

    def __str__(self):
        return self.name


class CompanyGroup(models.Model):
    name = models.CharField(max_length=72)
    companies = models.ManyToManyField(Company)

    def __str__(self):
        return self.name


class Invoice(models.Model):
    # pulled from Data Source
    number = models.CharField(max_length=32)
    date = models.DateField()
    customer_number = models.CharField(max_length=32)
    sale_type = models.CharField(max_length=16)
    bill_to_name = models.CharField(max_length=128)
    bill_to_address = models.CharField(max_length=256)
    bill_to_city = models.CharField(max_length=128)
    bill_to_state = models.CharField(max_length=8)
    bill_to_zip = models.CharField(max_length=16)
    ship_to_name = models.CharField(max_length=128)
    ship_to_address = models.CharField(max_length=256)
    ship_to_city = models.CharField(max_length=128)
    ship_to_state = models.CharField(max_length=8)
    ship_to_zip = models.CharField(max_length=16)
    ship_date = models.DateField(blank=True, null=True)
    payment_type = models.CharField(max_length=16)
    warehouse_code = models.CharField(max_length=16)
    taxable_amount = models.FloatField()
    nontaxable_amount = models.FloatField()
    freight_amount = models.FloatField()
    sales_tax_amount = models.FloatField()
    cost_of_sales = models.FloatField()
    batch = models.CharField(max_length=32)
    # requires computation from data
    amount_without_tax = models.FloatField()
    amount_with_tax = models.FloatField()
    profit = models.FloatField()
    # foreign keys
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.company) + "'s INV#" + str(self.number)

class Warehouse(models.Model):
    name = models.CharField(max_length=128)
    code = models.CharField(max_length=16)

    def __str__(self):
        return str(self.name) + " - " + str(self.code)

class EstablishedSite(models.Model):
    name = models.CharField(max_length=128)
    address = models.CharField(max_length=256)
    longitude = models.FloatField()
    latitude = models.FloatField()
    invoices = models.ManyToManyField(Invoice)

    def __str__(self):
        return str(self.name)