from django.db import models
from .frames_models import Frames


class Smile(models.Model):
    id = models.AutoField(primary_key=True)
    left_corner_photo = models.FloatField()
    right_corner_photo = models.FloatField()
    left_corner = models.FloatField()
    right_corner = models.FloatField()
    frame_id = models.OneToOneField(Frames, on_delete=models.CASCADE)

    def __str__(self):
        return f"Smile in Frame {self.frame.id}"
