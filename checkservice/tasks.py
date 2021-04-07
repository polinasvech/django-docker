from django_rq import job
import json
import requests
from base64 import b64encode
from django.core.files.base import ContentFile

from django.conf import settings
from .enums import CheckStatus

from .models import Check

# Генерация pdf из html с использованием wkhtmltopdf
@job
def make_pdf(check_pk, name='', html=''):
    if not name:
        return 'Error'
    encoding = 'utf-8'
    # меняем кодировку
    base64_bytes = b64encode(str.encode(html))
    base64_string = base64_bytes.decode(encoding)
    # подготавливаем данные для запроса
    data = {
        'contents': base64_string,
    }
    headers = {
         'Content-Type': 'application/json',
    }
    # отправляем запрос на http://<docker_host>:<port>/
    response = requests.post(settings.WKHTMLTOPDF_URL, data=json.dumps(data), headers=headers)
    print('RESPONSE ', response)
    check = Check.objects.get(pk=check_pk)
    # сохраняем PDF в файл
    check.pdf_file.save(settings.MEDIA_ROOT + '/pdf/' + name + '.pdf', ContentFile(response.content))
    # изменяем статус чека на Rendered
    check.status = CheckStatus.rendered.value[0]
    check.save()