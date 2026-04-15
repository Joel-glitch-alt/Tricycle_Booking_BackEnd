from django.db import models

class Driver(models.Model):
    full_name = models.CharField(max_length=255)
    vehicle = models.CharField(max_length=100)
    rating = models.FloatField(default=0.0)
    trips = models.IntegerField(default=0)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.full_name