# from django.contrib.auth.models import User
from django.db import models
from .enums import Role
from .userProfile_models import UserProfile
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver


class Auth(models.Model):
    id = models.OneToOneField(UserProfile, on_delete=models.CASCADE, primary_key=True)
    login = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    role = models.CharField(max_length=10, choices=[(role.value, role.name) for role in Role])

    def __str__(self):
        return f"{self.login}"

    def login_change(self, new_login):
        self.login = new_login
        self.save()

    def password_change(self, new_password):
        self.password = new_password
        self.save()

    @classmethod
    def create_auth(cls, user_id, login, password, role):
        auth = cls(id=user_id, login=login, password=password, role=role)
        auth.save()
        return auth

    # @receiver(pre_save, sender=User)
    # def check_user_existence(sender, instance, **kwargs):
    #     # Sprawdzamy czy użytkownik ma rolę doctor
    #     if instance.groups.filter(name='doctor').exists():
    #         return
    #     else:
    #         # Jeżeli użytkownik nie ma roli doctor, blokujemy rejestrację
    #         raise PermissionDenied("This user cannot register as a patient.")
    #
    # @receiver(post_save, sender=User)
    # def create_auth(sender, instance, created, **kwargs):
    #     # Sprawdzamy czy użytkownik ma rolę doctor
    #     if created and instance.groups.filter(name='doctor').exists():
    #         # Tworzymy rekord w tabeli Auth dla nowo zarejestrowanego użytkownika
    #         Auth.objects.create(user=instance, login=instance.username, password=instance.password,
    #                             role=Role.PATIENT.value)