# Generated by Django 5.0.6 on 2024-05-20 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FaceMotionMonitorApp', '0006_remove_doctorandpatient_doctor_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctorandpatient',
            name='doctor_id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='doctorandpatient',
            name='patient_id',
            field=models.IntegerField(),
        ),
    ]
