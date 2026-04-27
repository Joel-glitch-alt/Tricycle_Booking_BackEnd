from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('initialize/', views.InitializePaymentView.as_view(), name='initialize-payment'),
    path('verify/<str:reference>/', views.VerifyPaymentView.as_view(), name='verify-payment'),
    path('webhook/', views.paystack_webhook, name='paystack-webhook'),
]

