import json
from django.shortcuts import render

from .utils import make_html
from .models import Check, Printer
from .forms import CheckForm
from .enums import CheckStatus
from django.http import HttpResponse, JsonResponse


# Создание новых чеков по данным заказа
def create_checks(request):
    if request.method == "POST":
        order = json.loads(request.POST.get('order'))
        print(order, type(order))

        # Если у точки нет ни одного принтера - возвращает ошибку
        printers = Printer.objects.filter(point_id=order['point_id'])
        if not printers:
            return JsonResponse(
                {"error": "Для данной точки не настроено ни одного принтера"},
                status=400
            )
        # Если чеки для данного заказа уже были созданы - возвращает ошибку.
        if Check.objects.filter(order=order):
            return JsonResponse(
                {"error": "Для данного заказа уже созданы чеки"},
                status=400
            )
        for printer in printers:
            check = Check(printer_id=printer)
            data = {
                'type': printer.check_type,
                'order': order,
                'status': CheckStatus.new.value[0]
            }
            check.type = printer.check_type
            check.order = order
            check.status = CheckStatus.new.value[0]
            check.save()
            make_html(data, check.pk)

        return JsonResponse(
            {"detail": "Чеки успешно созданы"},
            status=200
        )
    else:
        checkform = CheckForm()
        return render(request, "create_checks.html", {"form": checkform})


# Список доступных чеков для печати
def new_checks(request):
    try:
        printer = Printer.objects.get(api_key=request.GET.get('api_key', None))
    except Printer.DoesNotExist:
        return HttpResponse(
            {"error": "Ошибка авторизации"},
            status=401
        )
    data = {'checks': []}
    for check in Check.objects.filter(printer_id=printer, status='r'):
        data['checks'].append({'id': check.pk})
    return JsonResponse(data)

# PDF-файл чека
def check(request):
    # Загружаем принтер, если не найден - возвращает ошибку
    try:
        printer = Printer.objects.get(api_key=request.GET.get('api_key', None))
    except Printer.DoesNotExist:
        return JsonResponse(
            {"error": "Ошибка авторизации"},
            status=401
        )
    # Загружаем чек, если не найден - возвращает ошибку
    try:
        check = Check.objects.get(printer_id=printer, pk=request.GET.get('check_id'))
    except Check.DoesNotExist:
        return JsonResponse(
            {"error": "Данного чека не существует"},
            status=4000
        )
    # Если к чеку не добавлен pdf - возвращает ошибку
    if not check.pdf_file:
        return JsonResponse(
            {"error": "Для данного чека не сгенерирован PDF-файл"},
            status=400
        )
    # Извлекаем бинарное содержимое PDF-файла
    try:
        file = open(str(check.pdf_file), 'rb')
        file_content = file.read()
        file.close()
    except FileNotFoundError:
        return JsonResponse(
            {"error": "Файл с PDF не смог быть прочитан"},
            status=500
        )

    # изменяем статус чека на Printed
    check.status = CheckStatus.printed.value[0]
    check.save()

    return HttpResponse(file_content, status=200, content_type='application/pdf')

# Начальная страница
def index(request):
    return render(request, "index.html")
