from django.db import models
from .recordings_models import Recordings


class Frames(models.Model):
    id = models.AutoField(primary_key=True)
    frame_number = models.IntegerField()
    timestamp = models.FloatField()
    x_center = models.FloatField()
    y_center = models.FloatField()
    recording_id = models.OneToOneField(Recordings, on_delete=models.CASCADE)

    def __str__(self):
        return f"Frame {self.frame_number} of Recording {self.recording.id}"

