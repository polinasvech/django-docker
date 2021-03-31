from django.db import models


class Printer(models.Model):
    name = models.CharField(max_length=255)
    api_key = models.CharField(max_length=36, unique=True)
    CHECK_TYPE_CHOICES = (
      ('k', 'kitchen'),
      ('c', 'client'),
    )
    check_type = models.CharField(max_length=1, choices=CHECK_TYPE_CHOICES)
    point_id = models.IntegerField()


class Check(models.Model):
    printer_id = models.ForeignKey('Printer', related_name='checks', on_delete=models.CASCADE)
    CHECK_TYPE_CHOICES = (
        ('k', 'kitchen'),
        ('c', 'client'),
    )
    type = models.CharField(max_length=1, choices=CHECK_TYPE_CHOICES)
    order = models.JSONField()
    STATUS_CHOICES = (
        ('n', 'new'),
        ('r', 'rendered'),
        ('p', 'printed')
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    pdf_file = models.FileField(upload_to='pdf/', null=True)
