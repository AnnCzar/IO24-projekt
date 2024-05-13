from django.contrib.auth.hashers import check_password
from rest_framework import serializers
from django.apps import apps

from FaceMotionMonitorApp.models import UserProfile
from FaceMotionMonitorApp.models.userProfile_models import Auth, Doctor, Patient, DoctorAndPatient


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'name', 'surname', 'email', 'pesel']


def validate_email(value):  # to check if email is taken
    if UserProfile.objects.filter(email=value).exists():
        raise serializers.ValidationError("Email already exists.")
    else:
        return False


class AuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auth
        fields = ['id', 'login', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}


def validate_login(value):  # to check if login is taken
    if Auth.objects.filter(login=value).exists():
        raise serializers.ValidationError("Login already exists.")
    else:
        return False


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['id', 'pwz_pwzf', 'user_id']


def validate_pwz_pwzf(value):  # to check if pwz is taken
    if Doctor.objects.filter(pwz_pwzf=value).exists():
        raise serializers.ValidationError("PWZ_PWZF already exists.")
    else:
        return False


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'date_of_birth', 'date_of_diagnosis', 'sex', 'user_id']


class DoctorAndPatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorAndPatient
        fields = ['id', 'doctor', 'patient']


def validate_pesel(value):  # to check if pesel of patient is in db
    if UserProfile.objects.filter(pesel=value).exists():
        return True
    else:
        return False


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
