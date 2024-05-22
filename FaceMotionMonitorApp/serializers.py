from django.contrib.auth.hashers import check_password
from rest_framework import serializers
from django.apps import apps
from django.contrib.auth.hashers import make_password
from FaceMotionMonitorApp.models import UserProfile
from FaceMotionMonitorApp.models.userProfile_models import Auth, Doctor, Patient, DoctorAndPatient, Recordings, Frames, \
    FrameLandmarks, RefPhotos, RefPhotoLandmarks, Smile


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


class AuthUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auth
        fields = ['login', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_login(self, value):
        if self.instance and self.instance.login == value:
            return value
        if Auth.objects.filter(login=value).exists():
            raise serializers.ValidationError("Login already exists.")
        return value

    def update(self, instance, validated_data):
        instance.login = validated_data.get('login', instance.login)
        instance.password = make_password(validated_data.get('password', instance.password))
        instance.save()
        return instance


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
        fields = ['id', 'patient_id', 'doctor_id']
    #


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



class FrameLandmarksSerializer(serializers.ModelSerializer):
    class Meta:
        model = FrameLandmarks
        fields = ['id', 'x_cord', 'y_cord', 'landmark_number', 'frame_id']


class SmileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Smile
        fields = ['id', 'left_corner_photo', 'right_corner_photo', 'left_corner', 'right_corner', 'frame_id']



class FramesSerializer(serializers.ModelSerializer):
    framelandmarks = FrameLandmarksSerializer(many=True)
    smile = SmileSerializer()

    class Meta:
        model = Frames
        fields = '__all__'

    def create(self, validated_data):
        landmarks_data = validated_data.pop('framelandmarks')
        smile_data = validated_data.pop('smile')
        frame = Frames.objects.create(**validated_data)

        for landmark_data in landmarks_data:
            FrameLandmarks.objects.create(frame=frame, **landmark_data)

        Smile.objects.create(frame=frame, **smile_data)

        return frame

class FrameLandmarksSerializer(serializers.ModelSerializer):
    class Meta:
        model = FrameLandmarks
        fields = ['id', 'x_cord', 'y_cord', 'landmark_number', 'frame_id']

class RecordingsSerializer(serializers.ModelSerializer):
    frames = FramesSerializer(many=True)

    class Meta:
        model = Recordings
        fields = '__all__'

    def create(self, validated_data):
        frames_data = validated_data.pop('frames')
        recording = Recordings.objects.create(**validated_data)

        for frame_data in frames_data:
            landmarks_data = frame_data.pop('framelandmarks')
            smile_data = frame_data.pop('smile')
            frame = Frames.objects.create(recording=recording, **frame_data)

            for landmark_data in landmarks_data:
                FrameLandmarks.objects.create(frame=frame, **landmark_data)

            Smile.objects.create(frame=frame, **smile_data)

        return recording
class RefPhotosSerializer(serializers.ModelSerializer):
    class Meta:
        model = RefPhotos
        fields = ['id', 'date', 'x_center', 'y_center', 'patient_id']


class RefPhotoLandmarksSerializer(serializers.ModelSerializer):
    class Meta:
        model = RefPhotoLandmarks
        fields = ['id', 'x_cord', 'y_cord', 'landmark_number', 'ref_photo']


