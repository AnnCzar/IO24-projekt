from django.contrib.auth.hashers import make_password
from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoginSerializer
from .models import Role
from .serializers import UserProfileSerializer, AuthSerializer, DoctorSerializer

# twoje funkcje/klasy widoków


class UserRegistration(views.APIView):
    def post(self, request):
        user_profile_serializer = UserProfileSerializer(data=request.data)

        if user_profile_serializer.is_valid():
            user_profile = user_profile_serializer.save()
            role_vale = Role[request.data['role']].value

            auth_data = {
                'login': request.data['login'],
                'password': make_password(request.data['password']),
                'role': role_vale,
                'id': user_profile.id  # Assuming user profile ID is used in Auth
            }
            auth_serializer = AuthSerializer(data=auth_data)

            if auth_serializer.is_valid():
                print("dziala")
                auth_serializer.save()

                # Check if the role is Doctor and handle Doctor data
                if Role[request.data['role']].value == Role.DOCTOR.value:
                    doctor_data = {
                        'pwz_pwzf': request.data['pwz_pwzf'],
                        'user_id': user_profile.id
                    }
                    doctor_serializer = DoctorSerializer(data=doctor_data)

                    if doctor_serializer.is_valid():
                        doctor_serializer.save()
                    else:
                        return Response(doctor_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
            else:
                print("niedziala")
                return Response(auth_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(user_profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoginSerializer

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            # Uwierzytelnienie użytkownika i rozpoczęcie sesji
            django_user = authenticate(request, username=user.login, password=request.data['password'])
            print(django_user)
            if django_user is not None:
                login(request, django_user)  # Rozpoczęcie sesji
                return Response({
                    'message': 'Login successful.',
                    'user_id': user.id,
                    'role': user.role
                }, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
