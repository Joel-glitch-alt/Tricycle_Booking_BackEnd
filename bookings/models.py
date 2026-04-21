from django.db import models
from django.conf import settings
from drivers.models import Driver

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    driver = models.ForeignKey(
        Driver,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    passengers = models.IntegerField(default=1)
    pickup_location = models.CharField(max_length=255, blank=True, default='') # ✅ new
    destination = models.CharField(max_length=255, blank=True, default='')     # ✅ new
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking {self.id} - {self.user} → {self.driver.full_name}"