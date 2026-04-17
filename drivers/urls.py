# drivers/urls.py
from django.urls import path
from . import views

app_name = 'drivers'

urlpatterns = [
    path('available/', views.AvailableDriversView.as_view(), name='available-drivers'),
    path('available/<int:pk>/', views.DriverDetailView.as_view(), name='driver-detail'),
]