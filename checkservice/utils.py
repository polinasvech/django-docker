from .tasks import make_pdf
from django.template.loader import render_to_string
import django_rq

# Генерация html-шаблона для новых чеков
def make_html(data, check_pk):
    template = 'kitchen_template.html' if data['type'] == 'k' \
        else 'client_template.html'
    html = render_to_string(template, data)
    check_type = 'kitchen' if data['type'] == 'k' else 'client'
    name = str(data['order']['id']) + '_' + check_type
    # with open(settings.MEDIA_ROOT + '/html/' + name + '.html', 'w') as static_file:
    #     static_file.write(html)
    #     static_file.close()
    django_rq.enqueue(make_pdf, check_pk, name, html)