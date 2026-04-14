from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import PasswordResetOTP, User


#    SIGNUP
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

                 # LOGIN
class LoginSerializer(serializers.Serializer):
    email    = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email    = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(username=email, password=password)

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



                 # FORGOT
class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError('No account found with this email.')
        return value



      # VERIFY OTP
class VerifyOTPSerializer(serializers.Serializer):
    """Step 2 — user submits the 6-digit code from their email"""
    email = serializers.EmailField()
    code  = serializers.CharField(max_length=6)

    def validate(self, attrs):
        try:
            user = User.objects.get(email__iexact=attrs['email'])
        except User.DoesNotExist:
            raise serializers.ValidationError({'email': 'No account found with this email.'})

        otp = PasswordResetOTP.objects.filter(
            user=user, is_used=False
        ).order_by('-created_at').first()

        if not otp or otp.code != attrs['code']:
            raise serializers.ValidationError({'code': 'Invalid OTP code.'})

        if not otp.is_valid():
            raise serializers.ValidationError({'code': 'OTP has expired. Please request a new one.'})

        attrs['user'] = user
        attrs['otp']  = otp
        return attrs




      # RESET PASSWORD
class ResetPasswordSerializer(serializers.Serializer):
    """Step 3 — user submits new password"""
    email            = serializers.EmailField()
    code             = serializers.CharField(max_length=6)
    new_password     = serializers.CharField(write_only=True, min_length=8, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({'new_password': 'Passwords do not match.'})

        try:
            user = User.objects.get(email__iexact=attrs['email'])
        except User.DoesNotExist:
            raise serializers.ValidationError({'email': 'No account found with this email.'})

        otp = PasswordResetOTP.objects.filter(
            user=user, is_used=False
        ).order_by('-created_at').first()

        if not otp or otp.code != attrs['code']:
            raise serializers.ValidationError({'code': 'Invalid or expired OTP.'})

        if not otp.is_valid():
            raise serializers.ValidationError({'code': 'OTP has expired. Please request a new one.'})

        attrs['user'] = user
        attrs['otp']  = otp
        return attrs