from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Check, Printer
from .serializers import CheckSerializer

@api_view(['POST'])
def create_check(request):
    order = request.data

    # Если у точки нет ни одного принтера - возвращает ошибку
    printers = Printer.objects.filter(point_id=order['point_id'])
    if not printers:
        return Response(
            {"detail": "Для данной точки не настроено ни одного принтера."},
            status=status.HTTP_400_BAD_REQUEST
        )
    # Если чеки для данного заказа уже были созданы - возвращает ошибку.
    order = request.data
    if Check.objects.filter(order=order):
        return Response(
            {"detail": "Для данного заказа уже созданы чеки."},
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

    return Response(
        {"detail": "Чеки успешно созданы."},
        status=status.HTTP_200_OK
    )

    # print('REQ ', printers)
    # serializer = CheckSerializer(data=request.data)
    #
    # if serializer.is_valid():
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
    # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
