from django_rq import job
import json
import requests
import os
from base64 import b64encode
from django.core.files.storage import default_storage

from django.conf import settings

from .models import Check

# Генерация pdf из html с использованием wkhtmltopdf
@job
def make_pdf(check_id, name='', html=''):
    if not name:
        return 'Error'
    # меняем кодировку
    html_b64 = b64encode(bytes(html, 'utf-8'))
    if not default_storage.exists(os.path.join(settings.MEDIA_ROOT, 'pdf', name, '.pdf')):
        # подготавливаем данные для запроса
        data = {
            'contents': html_b64.decode('utf-8'),
        }
        headers = {
             'Content-Type': 'application/json',
        }
        # отправляем запрос на http://<docker_host>:<port>/
        response = requests.post(settings.WKHTMLTOPDF_URL, data=json.dumps(data), headers=headers)
        #сохраняем файл
        with open(os.path.join(settings.MEDIA_ROOT, 'pdf', name+'.pdf'), 'wb') as f:
            f.write(response.content)

    check = Check.objects.get(pk=check_id)
    # добавляем PDF к чеку
    check.pdf_file = os.path.join(settings.MEDIA_ROOT, 'pdf',  name+'.pdf')
    # изменяем статус чека на Rendered
    check.status = Check.STATUS.RENDERED
    check.save()
