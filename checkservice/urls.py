from django.conf.urls import url

from checkservice import views

app_name = "checkservice"
# app_name will help us do a reverse look-up latter.
urlpatterns = [
    url('create_checks/', views.create_checks),
]