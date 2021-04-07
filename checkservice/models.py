from django.db import models
from django.contrib.postgres.fields import JSONField
from .enums import CheckTypes, CheckStatus

# Модель принтера
class Printer(models.Model):
    name = models.CharField(max_length=255)
    api_key = models.CharField(max_length=36, unique=True)
    check_type = models.CharField(max_length=1, choices=CheckTypes.choices())
    point_id = models.IntegerField()

    def __str__(self):
        return self.name

# Модель чека
class Check(models.Model):
    printer_id = models.ForeignKey('Printer', related_name='checks', on_delete=models.CASCADE)
    type = models.CharField(max_length=1, choices=CheckTypes.choices())
    order = JSONField()
    status = models.CharField(max_length=1, choices=CheckStatus.choices())
    pdf_file = models.FileField(blank=True, null=True)

    class Meta:
        unique_together = ('order', 'type', 'printer_id')
        indexes = [
            models.Index(fields=['order']),
        ]