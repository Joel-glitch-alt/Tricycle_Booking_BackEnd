# drivers/urls.py
from django.urls import path
from . import views

app_name = 'drivers'

urlpatterns = [
    path('drivers/available/', views.AvailableDriversView.as_view(), name='available-drivers'),
]