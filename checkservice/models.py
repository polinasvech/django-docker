from django.db import models
from django.contrib.postgres.fields import JSONField


class CHECKTYPE:
    KITCHEN = 'Kitchen'
    CLIENT = 'Client'


CHECKTYPE_CHOISES = [(CHECKTYPE.KITCHEN, 'Kitchen'), (CHECKTYPE.CLIENT, 'Client')]

# Модель принтера
class Printer(models.Model):
    name = models.CharField(max_length=16, verbose_name='название принтера')
    api_key = models.CharField(max_length=36, unique=True, verbose_name='ключ доступа к API')
    check_type = models.CharField(max_length=16, choices=CHECKTYPE_CHOISES, verbose_name='тип чека которые печатает принтер')
    point_id = models.IntegerField(verbose_name='точка к которой привязан принтер')

    def __str__(self):
        return self.name

# Модель чека
class Check(models.Model):
    class STATUS:
        NEW = 'New'
        RENDERED = 'Rendered'
        PRINTED = 'Printed'

    STATUS_CHOISES = [(STATUS.NEW, 'New'), (STATUS.RENDERED, 'Rendered'), (STATUS.PRINTED, 'Printed')]
    printer_id = models.ForeignKey('Printer', related_name='checks', on_delete=models.CASCADE, verbose_name='принтер')
    type = models.CharField(max_length=16, choices=CHECKTYPE_CHOISES, verbose_name='тип чека')
    order = JSONField(verbose_name='информация о заказе')
    status = models.CharField(max_length=16, choices=STATUS_CHOISES, verbose_name='статус чека')
    pdf_file = models.FileField(blank=True, null=True, verbose_name='ссылка на созданный PDF-файл')

    class Meta:
        unique_together = ('order', 'type', 'printer_id')
        indexes = [
            models.Index(fields=['order']),
        ]