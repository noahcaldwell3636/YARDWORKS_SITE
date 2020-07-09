from django.contrib import admin
from reports.models import Company, Invoice, CompanyGroup

# Register your models here.
admin.site.register(Company)
admin.site.register(Invoice)
admin.site.register(CompanyGroup)

