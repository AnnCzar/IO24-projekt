from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect, HttpResponse, StreamingHttpResponse
from rest_framework import views
from rest_framework.decorators import api_view

from .ai_model.brudnopis import VideoProcessor
from .backends.auth_backend import AuthBackend
from .models import Role, Sex, UserProfile
from .models.userProfile_models import Patient, Doctor, Auth, DoctorAndPatient
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


class AddPatient(views.APIView):

    #TODO add data validation (if pesel is in DB, check if the user is the patient)
    def post(self, request):
        role_vale = Role['PATIENT'].value
        pesel = request.data['pesel']

        if UserProfile.objects.filter(pesel=pesel).exists():  #patient exists
            user_profile = UserProfile.objects.get(pesel=pesel)
            user_id = user_profile.id

            patient = Patient.objects.get(user_id=user_id)
            patient_id = patient.id

            try:
                doctor_id = int(request.data['doctor_id'])
            except ValueError:
                return Response({"error": "Invalid doctor_id"}, status=status.HTTP_400_BAD_REQUEST)
            doctor_user_id = Doctor.objects.get(id=doctor_id).user_id

            if Auth.objects.get(id=doctor_user_id).role == Role['DOCTOR'].value:
                if DoctorAndPatient.objects.filter(doctor_id=doctor_id, patient_id=patient_id).exists():
                    # zabezpieczenie sprawdza czy dana para doktor - pacjent juz istenieje
                    return Response({'error': 'This doctor-patient pair already exists'},
                                    status=status.HTTP_400_BAD_REQUEST)

                patient_and_doctor_data = {
                    # to change - get if from info about session?
                    'patient_id': patient_id,
                    'doctor_id': doctor_id
                }

                patient_doctor_serializer = DoctorAndPatientSerializer(data=patient_and_doctor_data)

                if patient_doctor_serializer.is_valid():
                    patient_doctor_serializer.save()
                    return Response('Patient added to your list', status=status.HTTP_201_CREATED)
                else:
                    return Response(patient_doctor_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'User is not authorized, only doctor can add patient'},
                                status=status.HTTP_400_BAD_REQUEST)
        else:  #creating new patient
            user_profile_serializer = UserProfileSerializer(data=request.data)
            try:
                doctor_id = int(request.data['doctor_id'])
            except ValueError:
                return Response({"error": "Invalid doctor_id"}, status=status.HTTP_400_BAD_REQUEST)
            doctor_user_id = Doctor.objects.get(id=doctor_id).user_id

            if user_profile_serializer.is_valid() and Auth.objects.get(id=doctor_user_id).role == Role['DOCTOR'].value:
                user_profile = user_profile_serializer.save()

                auth_data = {
                    'login': None,
                    'password': None,
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

                if patient_serializer.is_valid() and Auth.objects.get(id=doctor_user_id).role == Role['DOCTOR'].value:

                    patient_serializer.save()

                    patient_and_doctor_data = {
                        # to change - get if from info about session?
                        'patient_id': patient_serializer.data['id'],
                        'doctor_id': doctor_id,
                    }
                    patient_doctor_serializer = DoctorAndPatientSerializer(data=patient_and_doctor_data)
                    if auth_serializer.is_valid() and patient_doctor_serializer.is_valid():
                        auth_serializer.save()
                        patient_doctor_serializer.save()

                        return Response('Patient added ', status=status.HTTP_201_CREATED)
                    else:
                        return Response(auth_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                else:
                    return Response({'error': 'User is not authorized, only doctor can add patient'},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(user_profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PatientRegistration(views.APIView):
    def patch(self, request):
        role_value = Role[request.data['role']].value  # to check if the data entered is ok
        pesel = request.data['pesel']
        name = request.data['name']
        surname = request.data['surname']
        email = request.data['email']

        login_new = request.data['login']  # to change in auth table
        password = request.data['password']

        if UserProfile.objects.filter(pesel=pesel).exists() and role_value == Role['PATIENT'].value:
            user_profile = UserProfile.objects.get(pesel=pesel)

            if user_profile.name == name and user_profile.surname == surname and user_profile.email == email:

                user_id = user_profile.id

                try:
                    user = Auth.objects.get(pk=user_id)
                except Auth.DoesNotExist:
                    return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

                new_data = {
                    'login': login_new,
                    'password': password,
                }
                serializer = AuthUpdateSerializer(user, data=new_data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response({"error": "DUPA"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'User profile data does not match.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('The patient with a given PESEL number is not in the database', status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):  #not working how I want - TO FIX

    #TODO fix it and read about session

    def post(self, request):
        login_value = request.data.get('login')
        password = request.data.get('password')

        auth_backend = AuthBackend()  # Tworzenie instancji własnego backendu
        user = auth_backend.authenticate(request, login=login_value, password=password)

        if user is not None:
              # Przekazanie nazwy backendu
            request.session['user_role'] = user.role
            return Response('User logged in', status=status.HTTP_200_OK)
            # return HttpResponseRedirect('/success-url/')  # Przekierowanie po zalogowaniu
        else:
            # Obsłuż błąd uwierzytelniania
            return Response('Nieprawidłowe dane logowania', status=400)


# class AddExamiantionView(views.APIView):   #its not working, dont delete
#     def post(self, request):
#         if 'patient_id' not in request.data:  # change it later, use session
#             return Response({'error': 'Patient ID is required'}, status=status.HTTP_400_BAD_REQUEST)
#
#         patient_id = request.data['patient_id']
#         try:
#             patient = UserProfile.objects.get(id=patient_id)
#         except UserProfile.DoesNotExist:
#             return Response({'error': 'Patient not found'}, status=status.HTTP_404_NOT_FOUND)
#
#         data = request.data
#         data['patient_id'] = patient.id
#
#         recording_serializer = RecordingsSerializer(data=data)
#         if recording_serializer.is_valid():
#             recording = recording_serializer.save()
#             return Response(recording_serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(recording_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddRecordingView(views.APIView):  #adding info about recordings to database
    def post(self, request):
        #here add a function that divides the recording into frames?
        #How to get  the time of the recording?

        recordings_serializer = RecordingsSerializer(data=request.data)
        if recordings_serializer.is_valid():
            recordings_serializer.save()
            return Response(recordings_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(recordings_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddFrameView(views.APIView): #adding info about frame to database
    def post(self, request):
        # move this code to 'generate_frame' and there refer to function which generete center point ???????
        frames_serializer = FramesSerializer(data=request.data)
        if frames_serializer.is_valid():
            frames_serializer.save()
            return Response(frames_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(frames_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddFrameLandmarksView(views.APIView):
    # IDEA: merge this code with code from 'AddFrameView'
    def post(self, request):
        frame_landmarks_serializer = FrameLandmarksSerializer(data=request.data)
        if frame_landmarks_serializer.is_valid():
            frame_landmarks_serializer.save()
            return Response(frame_landmarks_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(frame_landmarks_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddSmileView(views.APIView):
    # IDEA: merge this code with code from 'AddFrameView'
    def post(self, request):
        smile_serializer = SmileSerializer(data=request.data)
        if smile_serializer.is_valid():

            smile_serializer.save()
            return Response(smile_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(smile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def generate_frames():
    processor = VideoProcessor()  # call VideoProcessor class from AI model
    while True:
        frame = processor.process_frame()
        if frame is None:
            break
        yield (b'--frame\r\n'       # returns the processed frame as a byte string
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


class CapturePhotoView(APIView):
    def get(self, request):
        processor = VideoProcessor()
        _, img_bytes = processor.capture_photo()
        if img_bytes is None:
            return HttpResponse("Failed to capture photo.", status=500)
        return HttpResponse(img_bytes, content_type='image/jpeg')


@api_view(['GET'])   # streams the video frames to the client
def video_stream(request):
    return StreamingHttpResponse(generate_frames(), content_type='multipart/x-mixed-replace; boundary=frame')


@api_view(['GET'])  # just a message that recoding has started
def start_video_processing(request):
    return HttpResponse("Video processing started.")


class AddRefPhotoView(views.APIView):
    def post(self, request):
        ref_photos_serializer = RefPhotosSerializer(data=request.data)
        if ref_photos_serializer.is_valid():
            ref_photos_serializer.save()
            return Response(ref_photos_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(ref_photos_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddRefPhotoLandmarksView(views.APIView):
    # IDEA: merge this code with code from 'AddRefPhotoView'
    def post(self, request):
        ref_photos_landmarks_serializer = RefPhotoLandmarksSerializer(data=request.data)
        if ref_photos_landmarks_serializer.is_valid():
            ref_photos_landmarks_serializer.save()
            return Response(ref_photos_landmarks_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(ref_photos_landmarks_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
