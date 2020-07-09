from django.db import models



# Create your models here.
class Equipment(models.Model):
    # Core Info
    ident = models.CharField(max_length=6, default="None")
    key = models.CharField(max_length=32, default="None")
    desc = models.CharField(max_length=128, default="None")
    interval_unit = models.CharField(max_length=32, default="None")
    class_code = models.CharField(max_length=32, default="None")
    location_code = models.CharField(max_length=16, default="None")
    department_code = models.CharField(max_length=32, default="None")
    model = models.CharField(max_length=128, default="None")
    vin = models.CharField(max_length=64, default="None")
    make = models.CharField(max_length=64, default="None")
    size = models.CharField(max_length=32, default="None")
    licen = models.CharField(max_length=64, default="None")
    year = models.CharField(max_length=32, default="0000")
    # Service info
    oil_a = models.CharField(max_length=64, default="None")
    oil_b = models.CharField(max_length=64, default="None")
    fuel_a = models.CharField(max_length=64, default="None")
    fuel_b = models.CharField(max_length=64, default="None")
    air_in = models.CharField(max_length=64, default="None")
    air_out = models.CharField(max_length=64, default="None")
    cab_a = models.CharField(max_length=64, default="None")
    cab_b = models.CharField(max_length=64, default="None")
    water_sep = models.CharField(max_length=64, default="None")
    oil_gal = models.CharField(max_length=64, default="None")
    main_cost = models.CharField(max_length=64, default="None")
    serv_since2019 = models.CharField(max_length=64, default="None")
    current_units = models.CharField(max_length=32, default="None")
    # Equipment sheet info
    equipment_sheets = models.ForeignKey(EquipmentSheet, on_delete=models.CASCADE)
    # string representation
    def __str__(self):
        return self.ident

class EquipmentSheet(models.Model):
    name = models.CharField(max_length=164)
    date_submitted = models.DateTimeField()
    image = models.ImageField(upload_to='images/')

class MaintenanceOrder(models.Model):
    num = models.CharField(max_length=32)
    date_ordered = models.CharField(max_length=32)
    order_type = models.CharField(max_length=32)
    eq_key = models.CharField(max_length=32)
    eq_id = models.CharField(max_length=32)
    status = models.CharField(max_length=32)
    comment = models.TextField()
    completed_date = models.CharField(max_length=32)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, blank=True, null=True)
    # string representation
    def __str__(self):
        return "Maintenance Order #" + str(self.num)

class EquipmentInvoice(models.Model):
    num = models.CharField(max_length=32)
    date = models.CharField(max_length=32)
    vendor = models.CharField(max_length=32)
    amount = models.CharField(max_length=32)
    eq_key = models.CharField(max_length=32)
    eq_id = models.CharField(max_length=32)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, blank=True, null=True)
    #string representation
    def __str__(self):
        return "Invoice #" + str(self.num) + " for " + str(self.eq_id)

class Services(models.Model):
    # the data set should be 2019 and later
    num = models.CharField(max_length=64)
    key = models.CharField(max_length=64)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, blank=True, null=True)
    # string representation
    def __str__(self):
        return("Service #" + str(self.num))

class Usage(models.Model):
    # Data set is from 2019 and later
    key = models.CharField(max_length=32, default="None")
    units = models.CharField(max_length=32, default="None")
    date = models.CharField(max_length=32, default="None")
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, blank=True, null=True)
    # string representation

