from django.db import models
from .enums import Sex
from .refPhotos_models import RefPhotos


class UserProfile(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    pwz_pwzf = models.CharField(max_length=10, unique=True)
    email = models.EmailField(unique=True)
    pesel = models.CharField(max_length=11, unique=True)
    date_of_birth = models.DateField()
    date_of_diagnosis = models.DateField()
    sex = models.CharField(max_length=10, choices=[(sex.value, sex.name) for sex in Sex])
    ref_photo = models.OneToOneField(RefPhotos, on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.name} {self.surname}'s profile"

    @classmethod
    def create_user_profile(cls, user, name, surname, pwz_pwzf, email, pesel, date_of_birth, date_of_diagnosis, sex,
                            ref_photo):
        profile = cls(user=user, name=name, surname=surname, pwz_pwzf=pwz_pwzf, email=email, pesel=pesel,
                      date_of_birth=date_of_birth, date_of_diagnosis=date_of_diagnosis, sex=sex, ref_photo=ref_photo)
        profile.save()
        return profile
