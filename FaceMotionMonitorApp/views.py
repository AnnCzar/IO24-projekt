import base64
from datetime import date

import cv2
import numpy as np
from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect, HttpResponse, StreamingHttpResponse, JsonResponse
from django.views import View
from rest_framework import views
from rest_framework.decorators import api_view

from . import services
from .ai_model.brudnopis import VideoProcessor
from .backends.auth_backend import AuthBackend
from .models import Role, Sex, UserProfile
from .models.userProfile_models import Patient, Reports, DoctorAndPatient, Doctor, Auth
from .serializers import *
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import get_patient_details
from .ai_model import brudnopis


class DoctorRegistration(views.APIView):
    def post(self, request):
        role_vale = Role[request.data['role']].value
        pwz = request.data['pwz_pwzf']
        email = request.data['email']
        login1 = request.data['login']
        # checking if the user exists

        if role_vale == Role.DOCTOR.value and not (
                validate_email(email) and validate_login(login1) and validate_pwz_pwzf(pwz)):

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
                    errors = {**auth_serializer.errors, **doctor_serializer.errors}
                    return Response(errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(user_profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'Entered data already exist.'}, status=status.HTTP_400_BAD_REQUEST)


class AddPatient(views.APIView):

    #TODO add data validation (if pesel is in DB, check if the user is the patient)
    def post(self, request):
        role_vale = Role['PATIENT'].value
        pesel = request.data.get('pesel')

        try:
            # Get user_id from session
            user_id = request.session.get('user_id')


            doctor = Doctor.objects.get(user_id_id=user_id)  #tutaj jest problem
            print(doctor)
            doctor_id = doctor.id
        except Doctor.DoesNotExist:
            return Response({'error': 'User is not logged in or session has expired'},
                            status=status.HTTP_401_UNAUTHORIZED)
        # user_id = 32
        # doctor_id = 4
        if UserProfile.objects.filter(pesel=pesel).exists():  #patient exists
            user_profile = UserProfile.objects.get(pesel=pesel)
            user_id = user_profile.id

            patient = Patient.objects.get(user_id_id=user_id)
            patient_id = patient.id

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
            # try:
            #     doctor_id = int(request.data['doctor_id'])
            # except ValueError:
            #     return Response({"error": "Invalid doctor_id"}, status=status.HTTP_400_BAD_REQUEST)
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
            return Response('The patient with a given PESEL number is not in the database',
                            status=status.HTTP_400_BAD_REQUEST)


# class LoginView(APIView):
#     def post(self, request):
#         login_value = request.data.get('login')
#         password = request.data.get('password')
#
#         auth_backend = AuthBackend()
#         user = auth_backend.authenticate(request, login=login_value, password=password)
#
#         if user is not None:
#             # Przekazanie nazwy backendu
#             request.session['user_role'] = user.role
#             request.session['user_id'] = user.id_id
#             return Response('User logged in', status=status.HTTP_200_OK)
#         else:
#
#             return Response('Nieprawidłowe dane logowania', status=400)

class LoginView(APIView):
    def post(self, request):
        print(request)

        login_value = request.data.get('login')
        password = request.data.get('password')
        # print(login_value)
        # print(password)

        auth_backend = AuthBackend()
        user = auth_backend.authenticate(request, login=login_value, password=password)

        if user is not None:
            # Przekazanie nazwy backendu
            request.session['user_role'] = user.role
            request.session['user_id'] = user.id_id
            request.session.modified = True
            request.session.save()
            return Response({'message': 'User logged in', 'role': user.role, 'user_id': user.id_id}, status=status.HTTP_200_OK)
        else:

            return Response('Nieprawidłowe dane logowania', status=400)



class GetUserRoleView(View):
    def get(self, request):
        username = request.GET.get('login')
        try:
            user = Auth.objects.get(login=login)
            return JsonResponse({'role': user.role})
        except Auth.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)


def generate_frames():
    processor = VideoProcessor()  # call VideoProcessor class from AI model
    while True:
        frame = processor.process_frame()
        if frame is None:
            break
        yield (b'--frame\r\n'  # returns the processed frame as a byte string
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


# class CapturePhotoView(APIView):
#     def get(self, request):
#         processor = VideoProcessor()
#         _, img_bytes, landmark_list, distances, x_center, y_center = processor.capture_photo()
#         if img_bytes is None:
#             return HttpResponse("Failed to capture photo.", status=500)
#         return HttpResponse(img_bytes, content_type='image/jpeg')
#


@api_view(['POST'])
def capture_photo(request):
    data = request.data
    image_data = data['image']
    image_data = base64.b64decode(image_data.split(',')[1])
    np_arr = np.frombuffer(image_data, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    date_now = date.today()
    patient_id = 1  # example - change when session will be connect

    processor = VideoProcessor()
    img, img_bytes, landmark_list, distances, x_center, y_center = processor.capture_photo(img)

    ref_photo_data = {
        'date': date_now,
        'x_center': x_center,
        'y_center': y_center,
        'patient_id': patient_id
    }

    ref_photos_serializer = RefPhotosSerializer(data=ref_photo_data)

    if ref_photos_serializer.is_valid():
        ref_photos_serializer.save()

        for landmark, distance in distances.items():
            ref_photo_landmarks_data = {
                'x_cord': distance,
                'y_cord': 0,
                'landmark_number': landmark,
                'ref_photo': ref_photos_serializer.data['id']
            }
            ref_photos_landmarks_serializer = RefPhotoLandmarksSerializer(data=ref_photo_landmarks_data)
            if ref_photos_landmarks_serializer.is_valid():
                ref_photos_landmarks_serializer.save()
            else:
                return JsonResponse(ref_photos_landmarks_serializer.errors, status=400)

        return JsonResponse(ref_photos_serializer.data, status=201)
    else:
        return JsonResponse(ref_photos_serializer.errors, status=400)

@api_view(['GET'])  # streams the video frames to the client
def video_stream(request):
    return StreamingHttpResponse(generate_frames(), content_type='multipart/x-mixed-replace; boundary=frame')


@api_view(['GET'])  # just a message that recoding has started
def start_video_processing(request):
    return HttpResponse("Video processing started.")


@api_view(['POST'])  # new fun to add recordings
def add_recording(request):
    video_file = request.FILES['video']  # przesłanie nagrania z fronta
    video_data = video_file.read()

    # Process video through AI model
    processor = VideoProcessor()
    all_frames_data, frame_number_with_max_distance, landmark_list = processor.process_video(video_data)

    landmarks_data = []

    recording_data = {
        'date': date.today(),
        'time': 10,
        'patient_id': 1,  # example - change when session will be connect
    }

    recordings_serializer = RecordingsSerializer(data=recording_data)
    if recordings_serializer.is_valid():
        recording = recordings_serializer.save()

        # Save frames and landmarks to database

        for frame_number, frame_data in all_frames_data:

            if frame_number_with_max_distance == frame_number:
                landmark_numbers = [61, 291, 55, 285]
                for landmark_number in frame_data['landmark_number']:
                    if landmark_number in landmark_numbers:
                        landmarks_data.append({
                            'landmark_index': landmark_number.landmark_index,
                            'distance': landmark_number.distance,
                        })
            else:
                pass

            frame_serializer = FramesSerializer(data={
                'recording': recording.id,
                'frame_number': frame_number,
                'timestamp': frame_data['timestamp']
            })

            if frame_serializer.is_valid():
                frame = frame_serializer.save()

                for landmark_index, distance in frame_data['landmarks'].items():
                    landmark_serializer = FrameLandmarksSerializer(data={
                        'frame': frame.id,
                        'landmark_index': landmark_index,
                        'distance': distance,
                    })
                    if landmark_serializer.is_valid():
                        landmark_serializer.save()
        mouth, eyebrow_diff = calculate_difference(landmark_list, recording_data['patient_id'])
        report_data = {
            'date': date.today(),
            'difference_mouth': mouth,
            'difference_2': eyebrow_diff,
            'patient_id': recording_data['patient_id'],
        }
        Reports.objects.create(**report_data)

        return Response(recordings_serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(recordings_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# to trzeba wywalic stad i dac gdzies indziej
def calculate_difference(landmark_list, patient_id):
    # distances = [data['distance'] for data in landmarks_data]
    processor = VideoProcessor()

    #odleglosci z obecnego pomiaru
    # na razie mamy mouth - odległość między kącikami ust, bez porównaniado zdjęcia bazowego - można ewentualnie zmienić na koniec
    mouth = processor.calculate_distance_mouth(landmark_list)
    current_eyebrow = (processor.calculate_distance(landmark_list)[55] + processor.calculate_distance(landmark_list)[285]) / 2  #srednia odleglosci brwi od srodka

    #odleglosci z base photo
    ref_landmarks = services.get_ref_distances_for_landmarks(patient_id, [55, 285])
    # ref_mouth = processor.calculate_distance_mouth(ref_landmarks)
    ref_eyebrow = processor.calculate_distance(ref_landmarks[55] + processor.calculate_distance(ref_landmarks[285])) / 2 #srednia odleglosc brwi od srodka dla reference photo


    # roznica pomiedzy obecnym wynikiem a ze zdjecia bazowego
    eyebrow_diff = current_eyebrow - ref_eyebrow
    return mouth, eyebrow_diff


@api_view(['DELETE'])
def delete_user(request, user_id):
    try:
        # Usunięcie danych z tabeli Auth
        Auth.objects.filter(id=user_id).delete()

        # Sprawdzenie czy użytkownik jest pacjentem
        patient = Patient.objects.filter(user_id=user_id).first()
        if patient:
            patient_id = patient.id
            patient.delete()
            # Usunięcie przypisania do pacjenta
            DoctorAndPatient.objects.filter(patient_id=patient_id).delete()

        # Sprawdzenie czy użytkownik jest lekarzem
        doctor = Doctor.objects.filter(user_id=user_id).first()
        if doctor:
            doctor_id = doctor.id
            doctor.delete()
            # Usunięcie przypisania do lekarza
            DoctorAndPatient.objects.filter(doctor_id=doctor_id).delete()

        # Usunięcie danych z tabeli UserProfile
        UserProfile.objects.filter(id=user_id).delete()

        # Zwrócenie odpowiedzi HTTP
        return Response({'message': 'User deleted successfully'}, status=200)

    except Exception as e:
        # Obsługa wyjątku (np. gdy wystąpi problem z bazą danych)
        return Response({'error': 'Failed to delete user', 'details': str(e)}, status=500)


@api_view(['DELETE'])    # for admin
def delete_patient(request, patient_id):
    try:
        # Fetch the patient record
        patient = Patient.objects.filter(id=patient_id).first()
        if patient:
            # Get the user_id related to the patient
            user_id = patient.user_id_id

            # Delete data from the Auth table
            Auth.objects.filter(id=user_id).delete()

            # Delete the patient record
            patient.delete()

            # Delete the assignment from the DoctorAndPatient table
            DoctorAndPatient.objects.filter(patient_id=patient_id).delete()

            # Delete the related UserProfile record
            UserProfile.objects.filter(id=user_id).delete()

            # Check if the user is also a doctor and delete if exists
            # doctor = Doctor.objects.filter(user_id=user_id).first()
            # if doctor:
            #     doctor_id = doctor.id
            #     doctor.delete()
            #     # Delete the assignment from the DoctorAndPatient table
            #     DoctorAndPatient.objects.filter(doctor_id=doctor_id).delete()

            # Return HTTP response
            return Response({'message': 'Patient deleted successfully'}, status=200)

        else:
            return Response({'error': 'Patient not found'}, status=404)

    except Exception as e:
        # Handle exception (e.g., database issue)
        return Response({'error': 'Failed to delete patient', 'details': str(e)}, status=500)

# def get_ref_photo_landmarks(patient_id):
#     ref_photo = RefPhotos.objects.get(user_id=patient_id)
#     ref_photo_id = ref_photo.id
#     ref_photo_landmarks = RefPhotoLandmarks.objects.filter(ref_photo_id=ref_photo_id)
#     landmarks_list = []
#     for landmark in ref_photo_landmarks:
#         landmarks_list.append([landmark.landmark_number, landmark.distance])
#     return landmarks_list

@api_view(['GET'])
def get_patients_by_doctor(request):
    try:
        # Get user_id from session
        user_id = request.session.get('user_id')
        if not user_id:
            return Response({'error': 'User is not logged in or session has expired'},
                            status=status.HTTP_401_UNAUTHORIZED)

        # Retrieve the doctor associated with this user_id
        try:
            doctor = Doctor.objects.get(user_id=user_id)
        except Doctor.DoesNotExist:
            return Response({'error': 'No doctor found for this user'}, status=status.HTTP_404_NOT_FOUND)

        doctor_id = doctor.id

        # Find all patient IDs associated with the given doctor ID
        doctor_patient_relations = DoctorAndPatient.objects.filter(doctor_id=doctor_id)
        patient_ids = doctor_patient_relations.values_list('patient_id', flat=True)

        # Fetch patient data
        patients = Patient.objects.filter(id__in=patient_ids).select_related('user_id')

        # Serialize the patient data
        serializer = PatientSerializer(patients, many=True)

        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_reports_for_doctor_view(request, patient_id):
    try:
        # Get user_id from session
        user_id = request.session.get('user_id')
        if not user_id:
            return Response({'error': 'User is not logged in or session has expired'},
                            status=status.HTTP_401_UNAUTHORIZED)

        # Retrieve the doctor associated with this user_id
        try:
            doctor = Doctor.objects.get(user_id=user_id)
        except Doctor.DoesNotExist:
            return Response({'error': 'No doctor found for this user'}, status=status.HTTP_404_NOT_FOUND)

        doctor_id = doctor.id
        # Find all patient IDs associated with the given doctor ID
        if DoctorAndPatient.objects.filter(doctor_id=doctor_id, patient_id=patient_id).exists():
            reports = Reports.objects.filter(patient_id=patient_id)

            serializer = ReportsSerializer(reports, many=True)
            return Response(serializer.data)


    except Reports.DoesNotExist:
        return Response({'error': 'No reports found for this patient'}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def patient_details_view(request):
    user_doctor_id = request.session.get('user_id')
    details = get_patient_details(request)
    return Response(details, status=200)


@api_view(['GET'])
def get_reports_for_patient_view(request):
    try:
        # Get user_id from session
        user_id = request.session.get('user_id')
        if not user_id:
            return Response({'error': 'User is not logged in or session has expired'},
                            status=status.HTTP_401_UNAUTHORIZED)

        # Retrieve the doctor associated with this user_id
        try:
            patient_id = Patient.objects.get(user_id=user_id).id
        except Patient.DoesNotExist:
            return Response({'error': 'No patient found for this user'}, status=status.HTTP_404_NOT_FOUND)

        reports = Reports.objects.filter(patient_id=patient_id)

        serializer = ReportsSerializer(reports, many=True)
        return Response(serializer.data)


    except Reports.DoesNotExist:
        return Response({'error': 'No reports found for this patient'}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)



class LogoutView(APIView):
    def post(self, request):
        try:
            # Clear the session data
            request.session.flush()
            return Response({'message': 'User logged out successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_all_patients(request):
    try:

        patients = Patient.objects.all()
    except Patient.DoesNotExist:
        return Response({'error': 'No patient found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = PatientsSerializer(patients, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)