from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.password_validation import validate_password
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from .models import User


class SignupSerializer(serializers.ModelSerializer):
    password  = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, label='Confirm Password')

    class Meta:
        model  = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'phone_number',
            'password',
            'password2',
        ]

    def validate_username(self, value):
        if User.objects.filter(username__iexact=value).exists():
            raise serializers.ValidationError('Username is already taken')
        return value

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError('Email is already registered')
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': 'Passwords do not match'})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email    = serializers.EmailField()               # changed from username
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email    = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(username=email, password=password)  # Django authenticate still uses 'username' arg

        if not user:
            raise serializers.ValidationError('Invalid email or password')
        if not user.is_active:
            raise serializers.ValidationError('Your account has been disabled')

        attrs['user'] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()

    class Meta:
        model  = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'full_name',
            'phone_number',
            'role',
            'is_verified',
            'created_at',
        ]

#forget Password Serializer
class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        # Use iexact to stay consistent with how your SignupSerializer checks email
        if not User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError('No account found with this email.')
        return value
    


# ── Reset Password ────────────────────────────────────────────────────────────

class ResetPasswordSerializer(serializers.Serializer):
    uidb64           = serializers.CharField()
    token            = serializers.CharField()
    new_password     = serializers.CharField(write_only=True, min_length=8, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        # Check passwords match — same pattern as your SignupSerializer
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({'new_password': 'Passwords do not match'})

        # Decode uid and validate token here so the view stays clean
        try:
            uid  = force_str(urlsafe_base64_decode(attrs['uidb64']))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError({'uidb64': 'Invalid reset link.'})

        if not default_token_generator.check_token(user, attrs['token']):
            raise serializers.ValidationError({'token': 'Reset link is invalid or has expired.'})

        # Attach user so the view can call user.set_password() without re-fetching
        attrs['user'] = user
        return attrs