from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import random
from django.utils import timezone
from datetime import timedelta


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('passenger', 'Passenger'),
        ('driver', 'Driver'),
        ('admin', 'Admin'),
    )

    email        = models.EmailField(unique=True)
    username     = models.CharField(max_length=50, unique=True)
    first_name   = models.CharField(max_length=50)
    last_name    = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    role         = models.CharField(max_length=20, choices=ROLE_CHOICES, default='passenger')
    is_active    = models.BooleanField(default=True)
    is_verified  = models.BooleanField(default=False)
    is_staff     = models.BooleanField(default=False)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    # ↓ these two lines fix the clash
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='authentication_users',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='authentication_users',
        blank=True
    )

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return f"{self.email} ({self.role})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    

    # Password__RESETS
class PasswordResetOTP(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='otps')
    code       = models.CharField(max_length=6)
    is_used    = models.BooleanField(default=False)  # ← prevents reuse
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        not_expired = timezone.now() < self.created_at + timedelta(minutes=10)
        return not_expired and not self.is_used

    @staticmethod
    def generate_code():
        return str(random.randint(100000, 999999))  # always 6 digits

    def __str__(self):
        return f"{self.user.email} - {self.code}"