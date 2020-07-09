import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'YW_site.settings')

from django import setup
setup()

import os.path 
from reports.models import Company, Invoice
import xlrd, csv

Invoice.objects.all().delete()
Company.objects.all().delete()