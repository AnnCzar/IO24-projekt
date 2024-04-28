from django.db import models
from .refPhotos_models import RefPhotos


class RefPhotoLandmarks(models.Model):
    id = models.AutoField(primary_key=True)
    x_cord = models.FloatField()
    y_cord = models.FloatField()
    landmark_number = models.IntegerField()
    ref_photo = models.OneToOneField(RefPhotos, on_delete=models.CASCADE)

    def __str__(self):
        return f"Landmarks for Reference Photo {self.ref_photo.id}"