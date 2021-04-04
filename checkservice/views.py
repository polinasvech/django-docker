from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.conf import settings

from .models import Check, Printer
from .serializers import CheckSerializer
from django.template.loader import render_to_string
from .tasks import make_pdff
from django.http import HttpResponse
import django_rq


# Создание новых чеков по данным заказа
@api_view(['POST'])
def create_checks(request):
    order = request.data

    # Если у точки нет ни одного принтера - возвращает ошибку
    printers = Printer.objects.filter(point_id=order['point_id'])
    if not printers:
        return Response(
            {"error": "Для данной точки не настроено ни одного принтера."},
            status=status.HTTP_400_BAD_REQUEST
        )
    # Если чеки для данного заказа уже были созданы - возвращает ошибку.
    order = request.data
    if Check.objects.filter(order=order):
        return Response(
            {"error": "Для данного заказа уже созданы чеки."},
            status=status.HTTP_400_BAD_REQUEST
        )
    for printer in printers:
        check = Check(printer_id=printer)
        data = {
            'type': printer.check_type,
            'order': order,
            'status': 'n'
        }
        serializer = CheckSerializer(check, data=data)
        if serializer.is_valid():
            serializer.save()
        check.type = serializer.data['type']
        check.order = serializer.data['order']
        check.status = serializer.data['status']
        check.save()
        make_html(serializer.data, check.pk)

    return Response(
        {"detail": "Чеки успешно созданы."},
        status=status.HTTP_200_OK,
    )

# Список доступных чеков для печати
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

# PDF-файл чека
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
    # Извлекаем бинарное содержимое PDF-файла
    file = open(str(check.pdf_file), 'rb')
    file_content = file.read();
    file.close()

    # изменяем статус чека на Printed
    check.status = 'p'
    check.save()

    return HttpResponse(file_content, status=status.HTTP_200_OK, content_type='application/pdf')


# Генерация html-шаблона для новых чеков
def make_html(data, check_pk):
    template = 'kitchen_template.html' if data['type'] == 'k' \
        else 'client_template.html'
    html = render_to_string(template, data)
    check_type = 'kitchen' if data['type'] == 'k' else 'client'
    name = str(data['order']['id']) + '_' + check_type
    with open(settings.MEDIA_ROOT + '/html/' + name + '.html', 'w') as static_file:
        static_file.write(html)
        static_file.close()
    django_rq.enqueue(make_pdff, check_pk, name)
