from django.contrib import admin
from django.conf.urls import url, include

urlpatterns = [
    url('admin/', admin.site.urls),
    url('api/', include('checkservice.urls')),
    url('admin/rq/',  include('django_rq.urls'))
]
