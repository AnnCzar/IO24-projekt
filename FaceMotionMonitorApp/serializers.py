from django.contrib.auth.hashers import check_password
from rest_framework import serializers
from django.apps import apps

from FaceMotionMonitorApp.models import UserProfile
from FaceMotionMonitorApp.models.userProfile_models import Auth, Doctor


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'name', 'surname', 'email', 'pesel']

class AuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auth
        fields = ['id', 'login', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['id', 'pwz_pwzf', 'user_id']
class LoginSerializer(serializers.Serializer):
    login = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, data):
        login = data.get('login')
        password = data.get('password')

        try:
            user = Auth.objects.get(login=login)
        except Auth.DoesNotExist:
            raise serializers.ValidationError("Invalid login credentials.")

        if not check_password(password, user.password):
            raise serializers.ValidationError("Invalid login credentials.")

        data['user'] = user
        return data