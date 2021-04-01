from django.db import models
from .enums import CheckTypes


class Printer(models.Model):
    name = models.CharField(max_length=255)
    api_key = models.CharField(max_length=36, unique=True)
    for tag in CheckTypes:
        print("TAG", tag, type(tag), tag.value)
    check_type = models.CharField(max_length=1, choices=CheckTypes.choices())
    point_id = models.IntegerField()


class Check(models.Model):
    printer_id = models.ForeignKey('Printer', related_name='checks', on_delete=models.CASCADE)
    type = models.CharField(max_length=1, choices=CheckTypes.choices())
    order = models.JSONField()
    STATUS_CHOICES = (
        ('n', 'new'),
        ('r', 'rendered'),
        ('p', 'printed')
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    pdf_file = models.FileField(upload_to='pdf/', null=True)
