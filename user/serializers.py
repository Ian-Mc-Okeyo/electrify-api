from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from .models import UserProfile, MeterData, UserMeterNumber

class UserRegisterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']

class UserDetailsSerilizer(ModelSerializer):
    class Meta:
        model = User
        fields = ['email']

class ProfileCreateSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"

class MeterCreateSerializer(ModelSerializer):
    class Meta:
        model = UserMeterNumber
        fields = ['meterNumber', 'initialReading', 'user']

class DayDataSerializer(ModelSerializer):
    class Meta:
        model = MeterData
        fields = "__all__"
