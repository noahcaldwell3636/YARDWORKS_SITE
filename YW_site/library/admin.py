from django.contrib import admin
from library.models import Equipment, EquipmentInvoice, MaintenanceOrder, Services, Usage
# Register your models here.
admin.site.register(Equipment)
admin.site.register(EquipmentInvoice)
admin.site.register(MaintenanceOrder)
admin.site.register(Services)
admin.site.register(Usage)
