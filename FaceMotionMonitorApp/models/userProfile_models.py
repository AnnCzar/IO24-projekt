from django.db import models
from enum import Enum

from FaceMotionMonitorApp.models import Role


class Sex(Enum):
    MALE = 'male'
    FEMALE = 'female'


class UserProfile(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    pesel = models.CharField(max_length=11, unique=True)

class Doctor(models.Model):
    id = models.AutoField(primary_key=True)
    pwz_pwzf = models.CharField(max_length=10, unique=True)
    user_id = models.OneToOneField(UserProfile, on_delete=models.CASCADE)


class Patient(models.Model):
    id = models.AutoField(primary_key=True)
    date_of_birth = models.DateField()
    date_of_diagnosis = models.DateField()
    sex = models.CharField(max_length=10, choices=[(sex.value, sex.name) for sex in Sex])
    user_id = models.OneToOneField(UserProfile, on_delete=models.CASCADE)

class RefPhotos(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateTimeField()
    x_center = models.FloatField()
    y_center = models.FloatField()
    patient_id = models.OneToOneField(Patient, on_delete=models.CASCADE, null=True)

class DoctorAndPatient(models.Model):

    id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, related_name='patient_relations', on_delete=models.PROTECT)
    doctor = models.ForeignKey(Doctor, related_name='doctor_relations', on_delete=models.PROTECT)
    # def __str__(self):
    #     return f"Doctor: {self.doctor.username}, Patient: {self.patient.username}"

class Auth(models.Model):


    id = models.OneToOneField(UserProfile, on_delete=models.CASCADE, primary_key=True)
    login = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    role = models.CharField(max_length=10, choices=[(role.value, role.name) for role in Role])
class Recordings(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateTimeField()
    time = models.IntegerField()
    patient_id = models.OneToOneField(UserProfile, on_delete=models.PROTECT)

class Frames(models.Model):
    id = models.AutoField(primary_key=True)
    frame_number = models.IntegerField()
    timestamp = models.FloatField()
    x_center = models.FloatField()
    y_center = models.FloatField()
    recording_id = models.OneToOneField(Recordings, on_delete=models.CASCADE)

class FrameLandmarks(models.Model):
    id = models.AutoField(primary_key=True)
    x_cord = models.FloatField()
    y_cord = models.FloatField()
    landmark_number = models.IntegerField()
    frame_id = models.OneToOneField(Frames, on_delete=models.CASCADE)

class RefPhotoLandmarks(models.Model):
    id = models.AutoField(primary_key=True)
    x_cord = models.FloatField()
    y_cord = models.FloatField()
    landmark_number = models.IntegerField()
    ref_photo = models.OneToOneField(RefPhotos, on_delete=models.CASCADE)
class Smile(models.Model):
    id = models.AutoField(primary_key=True)
    left_corner_photo = models.FloatField()
    right_corner_photo = models.FloatField()
    left_corner = models.FloatField()
    right_corner = models.FloatField()
    frame_id = models.OneToOneField(Frames, on_delete=models.CASCADE)
