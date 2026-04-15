from django.db import models

from authentication.models import User

# Create your models here.
# models.py
class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    vehicle = models.CharField(max_length=100)
    rating = models.FloatField(default=0.0)
    trips = models.IntegerField(default=0)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.user.get_full_name()