from django.db import models


class RefPhotos(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateTimeField()
    x_center = models.FloatField()
    y_center = models.FloatField()
