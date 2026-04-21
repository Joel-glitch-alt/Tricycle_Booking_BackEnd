from rest_framework import serializers
from .models import Booking

class BookingSerializer(serializers.ModelSerializer):
    driver_name = serializers.CharField(
        source='driver.full_name', read_only=True
    )
    driver_vehicle = serializers.CharField(
        source='driver.vehicle', read_only=True
    )

    class Meta:
        model = Booking
        fields = [
            'id', 'driver', 'driver_name',
            'driver_vehicle', 'passengers',
            'pickup_location', 'destination', # ✅ added
            'status', 'created_at'
        ]
        read_only_fields = ['id', 'status', 'created_at']