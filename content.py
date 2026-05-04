# from django.shortcuts import render
# from rest_framework.permissions import AllowAny
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework import status

# from drivers.models import Driver
# from drivers.serializers import DriverSerializer

# class AvailableDriversView(APIView):
#     permission_classes = [AllowAny]

#     def get(self, request):
#         drivers = Driver.objects.filter(is_available=True)
#         serializer = DriverSerializer(drivers, many=True)
#         return Response(serializer.data)


# class DriverDetailView(APIView):  # ← add this
#     permission_classes = [AllowAny]

#     def get(self, request, pk):
#         try:
#             driver = Driver.objects.get(pk=pk)
#             serializer = DriverSerializer(driver)
#             return Response(serializer.data)
#         except Driver.DoesNotExist:
#             return Response({'error': 'Driver not found'}, status=status.HTTP_404_NOT_FOUND)



# def post(self, request):
#     booking_id = request.data.get('booking_id')
#     amount = request.data.get('amount')
    
#     # Add these debug lines
#     print(f"booking_id: {booking_id}")
#     print(f"amount: {amount}")
#     print(f"user: {request.user}")
#     print(f"user_id: {request.user.id}")