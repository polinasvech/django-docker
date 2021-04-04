from django.contrib import admin
from django.conf.urls import url, include

urlpatterns = [
    url('admin/', admin.site.urls),
    url('', include('checkservice.urls')),
    url('', include('checkapp.urls')),
    url('admin/rq/',  include('django_rq.urls'))
]
