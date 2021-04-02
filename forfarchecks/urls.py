from django.contrib import admin
from django.conf.urls import url, include

urlpatterns = [
    url('admin/', admin.site.urls),
    url('api/', include('checkservice.urls')),
    # path(r'^admin/rq/',  include('django_rq_dashboard.urls'))
]
