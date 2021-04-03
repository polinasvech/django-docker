from django_rq import job, get_worker, get_queue, get_scheduler
import json
import requests
from base64 import b64encode
from django.core.files import File

import redis
from django.conf import settings
import base64
import os

from .models import Check

redis_conn = redis.StrictRedis(host='', port='', db='', password='')
default_queue = get_queue('default', connection=redis_conn)


# scheduler = get_scheduler()

@job
def make_pdf(check_pk, name=''):
    if not name:
        return 'Error'
    encoding = 'utf-8'
    with open(settings.MEDIA_DIR + '/html/' + name + '.html', 'rb') as open_file:
        byte_content = open_file.read()
        base64_bytes = b64encode(byte_content)
        base64_string = base64_bytes.decode(encoding)
        data = {
            'contents': base64_string,
        }
        headers = {
            'Content-Type': 'application/json',

        }
        response = requests.post(settings.WKHTMLTOPDF_URL, data=json.dumps(data), headers=headers)

        check = Check.objects.get(pk=check_pk)
        print('CHECK ', check)
        print(name + '.pdf')

        # Save the response contents to a file
        with open(settings.MEDIA_DIR + '/pdf/' + name + '.pdf', 'wb') as f:
            f.write(response.content)
            f.close()

        with open(settings.MEDIA_DIR + '/pdf/' + name + '.pdf', encoding='utf-8', errors='ignore') as f:
            check.pdf_file.save(name + '.pdf', File(f))
            f.close()

        check.status = 'r'
        check.save()

        # Удаляем html
        if os.path.exists(settings.MEDIA_DIR + '/html/' + name + '.html'):
            os.remove(settings.MEDIA_DIR + '/html/' + name + '.html')
        else:
            print("The file does not exist")

        try:
            return + '<<<Debug task>>>'
        except TypeError:
            return 'no tasks now'


make_pdf.delay()

# @job
# def debug_scheduled_task():
#     raise ValueError('Hey man, shit broke')
#     # return 'Scheduled task'


# Delete any existing jobs in the scheduler when the app starts up
'''
for job in scheduler.get_jobs():
    job.delete()
'''

# enqueue(debug_task)
# worker = get_worker()
# print('WORK ', worker.name, worker.hostname, worker.queues)
# worker.work(burst=True)
# burst=True
