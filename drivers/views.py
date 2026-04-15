from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from drivers.models import Driver
from drivers.serializers import DriverSerializer

# Create your views here.
# views.py

class AvailableDriversView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        drivers = Driver.objects.filter(is_available=True)
        serializer = DriverSerializer(drivers, many=True)
        return Response(serializer.data)