from django.contrib.auth.hashers import make_password
from rest_framework import views
from .models import Role, Sex
from .serializers import *
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoginSerializer


# twoje funkcje/klasy widoków


class DoctorRegistration(views.APIView):
    def post(self, request):
        role_vale = Role[request.data['role']].value
        pwz = request.data['pwz_pwzf']
        email = request.data['email']
        login1 = request.data['login']
        # checking if the user exists

        if role_vale == Role.DOCTOR.value and validate_email(email) == False and validate_login(
                login1) == False and validate_pwz_pwzf(pwz) == False:

            user_profile_serializer = UserProfileSerializer(data=request.data)
            if user_profile_serializer.is_valid():
                user_profile = user_profile_serializer.save()

                auth_data = {
                    'login': request.data['login'],
                    'password': make_password(request.data['password']),
                    'role': role_vale,
                    'id': user_profile.id  # Assuming user profile ID is used in Auth
                }

                doctor_data = {
                    'pwz_pwzf': request.data['pwz_pwzf'],
                    'user_id': user_profile.id
                }
                auth_serializer = AuthSerializer(data=auth_data)
                doctor_serializer = DoctorSerializer(data=doctor_data)

                if user_profile_serializer.is_valid() and doctor_serializer.is_valid() and auth_serializer.is_valid():

                    auth_serializer.save()
                    doctor_serializer.save()
                    return Response(auth_serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(doctor_serializer.errors or auth_serializer.errors,
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(user_profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'Entered data already exist.'}, status=status.HTTP_400_BAD_REQUEST)



class AddPatient(APIView):

    #TODO add data validation (if pesel is in DB, check if the user is the patient)
    def post(self, request):

        role_vale = Role['PATIENT'].value
        pesel = request.data['pesel']

        if UserProfile.objects.filter(pesel=pesel).exists():
            user_profile = UserProfile.objects.get(pesel=pesel)
            user_id = user_profile.id
            patient = Patient.objects.get(user_id=user_id)
            patient_id = patient.id
            print(type(patient_id))
            try:
                idf = int(request.data['doctor_id'])
            except ValueError:
                return Response({"error": "Nieprawidłowy doctor_id"}, status=status.HTTP_400_BAD_REQUEST)
            patient_and_doctor_data = {
                'doctor_id': idf,  # to change - get if from info about session?
                'patient_id': patient_id
            }
            print(type(idf))

            patient_doctor_serializer = DoctorAndPatientSerializer(data=patient_and_doctor_data)

            if patient_doctor_serializer.is_valid():
                patient_doctor = patient_doctor_serializer.save()
                return Response('Patient added', status=status.HTTP_201_CREATED)
            else:
                return Response(patient_doctor_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            user_profile_serializer = UserProfileSerializer(data=request.data)
            if user_profile_serializer.is_valid():
                user_profile = user_profile_serializer.save()

                auth_data = {
                    'login': 'null',
                    'password': 'null',
                    'role': role_vale,
                    'id': user_profile.id  # Assuming user profile ID is used in Auth
                }

                patient_data = {
                    'date_of_birth': request.data['date_of_birth'],
                    'date_of_diagnosis': request.data['date_of_diagnosis'],
                    'sex': Sex[request.data['sex']].value,
                    'user_id': user_profile.id
                }

                auth_serializer = AuthSerializer(data=auth_data)

                patient_serializer = PatientSerializer(data=patient_data)

                if patient_serializer.is_valid():

                    patient_serializer.save()

                    patient_and_doctor_data = {
                        'doctor_id': request.data['doctor_id'],  # to change - get if from info about session?
                        'patient_id': patient_serializer.data['id']
                    }
                    patient_doctor_serializer = DoctorAndPatientSerializer(data=patient_and_doctor_data)
                    if auth_serializer.is_valid() and patient_doctor_serializer.is_valid():
                        auth_serializer.save()
                        patient_doctor_serializer.save()


                        return Response('Patient added', status=status.HTTP_201_CREATED)
                    else:
                        return Response(auth_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                else:
                    return Response(auth_serializer.errors,
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(user_profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#
#
# class AddPatient(APIView):
#
#     #TODO add data validation(if pesel is in DB check if the user is the patient)
#     def post(self, request):
#
#         role_vale = Role['PATIENT'].value
#         pesel = request.data['pesel']
#
#         if UserProfile.objects.filter(pesel=pesel).exists():
#             user_profile = UserProfile.objects.get(pesel=pesel)
#             user_id = user_profile.id
#             patient = Patient.objects.get(user_id=user_id)
#             patient_id = patient.id
#
#             patient_and_doctor_data = {
#                 'doctor_id': request.data['doctor_id'],  # to change - get if from info about session?
#                 'patient_id': patient_id
#             }
#
#             patient_doctor_serializer = DoctorAndPatientSerializer(data=patient_and_doctor_data)
#             if patient_doctor_serializer.is_valid():
#                 patient_doctor = patient_doctor_serializer.save()
#                 return Response('Patient added', status=status.HTTP_201_CREATED)
#             else:
#                 return Response(patient_doctor_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#         else:
#
#             user_profile_serializer = UserProfileSerializer(data=request.data)
#             if user_profile_serializer.is_valid():
#                 user_profile = user_profile_serializer.save()
#
#                 auth_data = {
#                     'login': 'null',
#                     'password': 'null',
#                     'role': role_vale,
#                     'id': user_profile.id  # Assuming user profile ID is used in Auth
#                 }
#
#                 patient_data = {
#                     'date_of_birth': request.data['date_of_birth'],
#                     'date_of_diagnosis': request.data['date_of_diagnosis'],
#                     'sex': Sex[request.data['sex']].value,
#                     'user_id': user_profile.id
#                 }
#
#                 auth_serializer = AuthSerializer(data=auth_data)
#
#                 patient_serializer = PatientSerializer(data=patient_data)
#
#                 if patient_serializer.is_valid():
#
#                     patient_serializer.save()
#
#                     patient_and_doctor_data = {
#                         'doctor_id': request.data['doctor_id'],  # to change - get if from info about session?
#                         'patient_id': patient_serializer.data['id']
#                     }
#                     patient_doctor_serializer = DoctorAndPatientSerializer(data=patient_and_doctor_data)
#                     if auth_serializer.is_valid() and patient_doctor_serializer.is_valid():
#                         auth_serializer.save()
#                         patient_doctor_serializer.save()
#
#                         return Response('Patient added', status=status.HTTP_201_CREATED)
#                     else:
#                         return Response(auth_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#                 else:
#                     return Response(auth_serializer.errors,
#                                     status=status.HTTP_400_BAD_REQUEST)
#             else:
#                 return Response(user_profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class PatientRegistration(views.APIView):
#     def post(self, request):
#         role_vale = Role[request.data['role']].value
#         pesel = request.data['pesel']
#         if UserProfile.objects.filter(pesel=pesel).exists():
#             user_profile = UserProfile.objects.get(pesel=pesel)
#             user_id = user_profile.id
#             patient = Patient.objects.get(user_id=user_id)
#             patient_id = patient.id
#             auth = Auth.objects(id=user_id)
#             if auth.role == Role.PATIENT.value:
#
#
#
#
#
#         else:
#             return Response('The patient with a given PESEL number is not in the database', status=status.HTTP_400_BAD_REQUEST)



class LoginView(APIView):   #not working how I want - TO FIX

    #TODO fix it and read about session
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
