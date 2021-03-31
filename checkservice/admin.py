from django.contrib import admin

from .models import Printer, Check

admin.site.register(Printer)
admin.site.register(Check)