from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse


def root(request):
    return JsonResponse({'message': 'Tricycle backend is running!'})


urlpatterns = [
    path('admin/',  admin.site.urls),
    path('',        root),
    path('auth/',   include('authentication.urls', namespace='authentication')),
    path('api/', include('drivers.urls', namespace='drivers')),
    # path('drivers/', include('drivers.urls', namespace='drivers')),
    # path('rides/', include('rides.urls', namespace='rides')),
    # path('notifications/', include('notifications.urls', namespace='notifications')),
]