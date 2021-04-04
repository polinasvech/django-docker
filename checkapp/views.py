from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core import serializers

from checkservice.models import Check, Printer
from checkservice.serializers import CheckSerializer

@api_view(['GET'])
def new_checks(self):
    try:
        printer = Printer.objects.get(api_key=self.query_params.get('api_key', None))
    except Printer.DoesNotExist:
        return Response(
            {"error": "Ошибка авторизации"},
            status=status.HTTP_401_UNAUTHORIZED
        )
    data = {'checks': []}
    for check in Check.objects.filter(printer_id=printer, status='r'):
        data['checks'].append({'id': check.pk})
    return Response(data)

@api_view(['GET'])
def check(self):
    import base64
    # Загружаем принтер, если не найден - возвращает ошибку
    try:
        printer = Printer.objects.get(api_key=self.query_params.get('api_key', None))
    except Printer.DoesNotExist:
        return Response(
            {"error": "Ошибка авторизации"},
            status=status.HTTP_401_UNAUTHORIZED
        )
    # Загружаем чек, если не найден - возвращает ошибку
    try:
        check = Check.objects.get(printer_id=printer, pk=self.query_params.get('check_id'))
    except Check.DoesNotExist:
        return Response(
            {"error": "Данного чека не существует"},
            status=status.HTTP_400_BAD_REQUEST
        )
    # Если к чеку не добавлен pdf - возвращает ошибку
    if not check.pdf_file:
        return Response(
            {"error": "Для данного чека не сгенерирован PDF-файл"},
            status=status.HTTP_400_BAD_REQUEST
        )
    check.status = 'p'
    check.save()
    file = open(str(check.pdf_file), 'rb')
    file_encoded = base64.b64encode(file.read())
    return Response(file_encoded, content_type='application/pdf')