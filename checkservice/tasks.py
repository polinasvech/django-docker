from django_rq import job, get_queue
import json
import requests
from base64 import b64encode
from django.core.files import File

import redis
from django.conf import settings
import os

from .models import Check

redis_conn = redis.StrictRedis(host='', port='', db='', password='')
default_queue = get_queue('default', connection=redis_conn)

# Генерация pdf из html с использованием wkhtmltopdf
@job
def make_pdf(check_pk, name=''):
    if not name:
        return 'Error'
    encoding = 'utf-8'
    with open(settings.MEDIA_ROOT + '/html/' + name + '.html', 'rb') as open_file:
        # меняет кодировку
        byte_content = open_file.read()
        base64_bytes = b64encode(byte_content)
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

        check = Check.objects.get(pk=check_pk)

        with open(settings.MEDIA_ROOT + '/pdf/' + name + '.pdf', 'wb') as f:
            f.write(response.content)
            f.close()

        with open(settings.MEDIA_ROOT + '/pdf/' + name + '.pdf', encoding='utf-8', errors='ignore') as f:
            check.pdf_file.save(name + '.pdf', File(f))
            f.close()
        # изменяем статус чека на Rendered
        check.status = 'r'
        check.save()

        # Удаляем html
        if os.path.exists(settings.MEDIA_ROOT + '/html/' + name + '.html'):
            os.remove(settings.MEDIA_ROOT + '/html/' + name + '.html')
        else:
            print("The file does not exist")
