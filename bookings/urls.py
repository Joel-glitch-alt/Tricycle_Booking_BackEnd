from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('create/', views.CreateBookingView.as_view(), name='create-booking'),
    path('my/', views.UserBookingsView.as_view(), name='user-bookings'),
]