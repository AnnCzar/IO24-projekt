from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

from FaceMotionMonitorApp.models.userProfile_models import Auth
User = get_user_model()

class AuthBackend(object):
    def authenticate(self, request, login=None, password=None):

        try:
            user = Auth.objects.get(login=login)
            if check_password(password, user.password):
                return user
        except Auth.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Auth.objects.get(pk=user_id)
        except Auth.DoesNotExist:
            return None

