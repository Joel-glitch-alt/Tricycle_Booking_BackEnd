from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from drivers.models import Driver
from rest_framework import status
from drivers.serializers import DriverSerializer

# Create your views here.
# views.py

class AvailableDriversView(APIView):
    permission_classes = [AllowAny]   #IsAuthenticated   ]

    def get(self, request):
        drivers = Driver.objects.filter(is_available=True)
        serializer = DriverSerializer(drivers, many=True)
        return Response(serializer.data)
    

    
#Getting Driver By Id
class DriverDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        try:
            driver = Driver.objects.get(pk=pk)
            serializer = DriverSerializer(driver)
            return Response(serializer.data)
        except Driver.DoesNotExist:
            return Response({'error': 'Oops....Driver not found'}, status =status.HTTP_404_NOT_FOUND)

    
    