from django.db import models
from .frames_models import Frames


class FrameLandmarks(models.Model):
    id = models.AutoField(primary_key=True)
    x_cord = models.FloatField()
    y_cord = models.FloatField()
    landmark_number = models.IntegerField()
    frame_id = models.OneToOneField(Frames, on_delete=models.CASCADE)


    def __str__(self):
        return f"FrameLandmarks for Frame: {self.frame.id}"
