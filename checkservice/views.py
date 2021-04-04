from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.conf import settings

from .models import Check, Printer
from .serializers import CheckSerializer
from django.template.loader import render_to_string
from .tasks import make_pdf
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
    print('PRINTERSSSS ', printers)
    for printer in printers:
        print('PRINTER ', printer)
        check = Check(printer_id=printer)
        data = {
            'type': printer.check_type,
            'order': order,
            'status': 'n'
        }
        serializer = CheckSerializer(check, data=data)
        if serializer.is_valid():
            serializer.save()
        print('VALDATA ', serializer.data)
        check.type = serializer.data['type']
        check.order = serializer.data['order']
        check.status = serializer.data['status']
        print('STATUS ', check.type)
        check.save()
        make_html(serializer.data, check.pk)

    return Response(
        {"detail": "Чеки успешно созданы."},
        status=status.HTTP_200_OK
    )


# Генерация html-шаблона для новых чеков
def make_html(data, check_pk):
    template = 'kitchen_template.html' if data['type'] == 'k' \
        else 'client_template.html'
    html = render_to_string(template, data)
    check_type = 'kitchen' if data['type'] == 'k' else 'client'
    name = str(data['order']['id']) + '_' + check_type
    print("ORDER ", data['order'])
    with open(settings.MEDIA_ROOT + '/html/' + name + '.html', 'w') as static_file:
        static_file.write(html)
        static_file.close()
    django_rq.enqueue(make_pdf, check_pk, name)
