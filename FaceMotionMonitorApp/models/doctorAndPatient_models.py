from django.db import models
from django.contrib.auth.models import User


class DoctorAndPatient(models.Model):
    id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(User, related_name='patient_relations', on_delete=models.PROTECT)
    doctor = models.ForeignKey(User, related_name='doctor_relations', on_delete=models.PROTECT)
    def __str__(self):
        return f"Doctor: {self.doctor.username}, Patient: {self.patient.username}"



