from django.conf.urls import url

from checkapp import views

app_name = "checkapp"
# app_name will help us do a reverse look-up latter.
urlpatterns = [
    url('new_checks/', views.new_checks),
    url('check/', views.check),
]