# serializers.py
from rest_framework import serializers

from drivers.models import Driver


class DriverSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = Driver
        fields = ['id', 'name', 'vehicle', 'rating', 'trips', 'is_available']

    def get_name(self, obj):
        return obj.user.get_full_name()