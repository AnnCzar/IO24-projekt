# Generated by Django 5.0.4 on 2024-04-28 15:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('surname', models.CharField(max_length=100)),
                ('pwz_pwzf', models.CharField(max_length=10, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('pesel', models.CharField(max_length=11, unique=True)),
                ('date_of_birth', models.DateField()),
                ('date_of_diagnosis', models.DateField()),
                ('sex', models.CharField(choices=[('male', 'MALE'), ('female', 'FEMALE')], max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Frames',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('frame_number', models.IntegerField()),
                ('timestamp', models.FloatField()),
                ('x_center', models.FloatField()),
                ('y_center', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='RefPhotos',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateTimeField()),
                ('x_center', models.FloatField()),
                ('y_center', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Auth',
            fields=[
                ('id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='FaceMotionMonitorApp.userprofile')),
                ('login', models.CharField(max_length=100, unique=True)),
                ('password', models.CharField(max_length=100)),
                ('role', models.CharField(choices=[('admin', 'ADMIN'), ('doctor', 'DOCTOR'), ('patient', 'PATIENT')], max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='DoctorAndPatient',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='doctor_relations', to=settings.AUTH_USER_MODEL)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='patient_relations', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FrameLandmarks',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('x_cord', models.FloatField()),
                ('y_cord', models.FloatField()),
                ('landmark_number', models.IntegerField()),
                ('frame_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='FaceMotionMonitorApp.frames')),
            ],
        ),
        migrations.CreateModel(
            name='Recordings',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateTimeField()),
                ('time', models.IntegerField()),
                ('patient_id', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='frames',
            name='recording_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='FaceMotionMonitorApp.recordings'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='ref_photo',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='FaceMotionMonitorApp.refphotos'),
        ),
        migrations.CreateModel(
            name='RefPhotoLandmarks',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('x_cord', models.FloatField()),
                ('y_cord', models.FloatField()),
                ('landmark_number', models.IntegerField()),
                ('ref_photo', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='FaceMotionMonitorApp.refphotos')),
            ],
        ),
        migrations.CreateModel(
            name='Smile',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('left_corner_photo', models.FloatField()),
                ('right_corner_photo', models.FloatField()),
                ('left_corner', models.FloatField()),
                ('right_corner', models.FloatField()),
                ('frame_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='FaceMotionMonitorApp.frames')),
            ],
        ),
    ]