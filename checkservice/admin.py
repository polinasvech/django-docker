from django.contrib import admin

from checkservice.models import Check, Printer
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter, ChoiceDropdownFilter


class CheckAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'type', 'status', 'printer_name', 'point')
    # Фильтр чеков по статусу, типу, принтеру
    list_filter = (
        ('status', ChoiceDropdownFilter),
        ('type', ChoiceDropdownFilter),
        ('printer_id', RelatedDropdownFilter),
    )
    search_fields = ('status', 'type', 'printer_id__id')

    def order_number(self, obj):
        return 'Order ' + str(obj.order['id'])

    def printer_name(self, obj):
        return obj.printer_id.name

    def point(self, obj):
        return obj.printer_id.point_id


class PrinterAdmin(admin.ModelAdmin):
    list_display = ('name', 'check_type', 'point_id', 'api_key')

admin.site.register(Check, CheckAdmin)
admin.site.register(Printer, PrinterAdmin)