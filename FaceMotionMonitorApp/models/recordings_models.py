from django.contrib.auth.models import User
from django.db import models


class Recordings(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateTimeField()
    time = models.IntegerField()
    patient_id = models.OneToOneField(User, on_delete=models.PROTECT)

    def __str__(self):
        return f"Recording {self.id} - Patient: {self.patient.username}"