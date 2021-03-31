from django.urls import path

from checkservice import views

app_name = "checkservice"
# app_name will help us do a reverse look-up latter.
urlpatterns = [
    path('create_checks/', views.create_checks),
]