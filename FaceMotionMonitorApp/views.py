import base64
from datetime import date, datetime
import os
import cv2
import numpy as np
from django.core.files.storage import default_storage
from django.http import HttpResponseRedirect, HttpResponse, StreamingHttpResponse, JsonResponse, FileResponse
from django.views import View
from rest_framework import views
from rest_framework.decorators import api_view
from .ai_model.reports.report import create_report
from . import services
from .ai_model.brudnopis import VideoProcessor
from .backends.auth_backend import AuthBackend
from .models import Role, Sex, UserProfile
from .serializers import *
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import get_patient_details
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import AllowAny


class DoctorRegistration(views.APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Registers a new doctor",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'login': openapi.Schema(type=openapi.TYPE_STRING, description='Login for the doctor'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password for the doctor'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email address of the doctor'),
                'pwz_pwzf': openapi.Schema(type=openapi.TYPE_STRING, description='PWZ number of the doctor'),
            },
            required=['login', 'password', 'email', 'pwz_pwzf']
        ),
        responses={
            201: 'Created',
            400: 'Bad Request'
        }
    )
    def post(self, request):
        """
                Registers a new doctor.

                This method handles the registration process for a new doctor. It validates the input data,
                creates the necessary user profile, authentication data, and doctor profile, and saves them
                to the database.

                Args:
                - request (Request): The request object containing doctor data.

                Returns:
                - Response: A response with the authentication data if registration is successful, otherwise an error message.
                """
        request.data['role'] = 'DOCTOR'
        role_value = Role[request.data['role']].value
        pwz = request.data['pwz_pwzf']
        email = request.data['email']
        login1 = request.data['login']
        # checking if the user exists

        if role_value == Role.DOCTOR.value and not (
                validate_email(email) and validate_login(login1) and validate_pwz_pwzf(pwz)):

            user_profile_serializer = UserProfileSerializer(data=request.data)
            if user_profile_serializer.is_valid():
                user_profile = user_profile_serializer.save()

                auth_data = {
                    'login': request.data['login'],
                    'password': make_password(request.data['password']),
                    'role': role_value,
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
    permission_classes = [AllowAny]  # Allows access to any user

    @swagger_auto_schema(
        operation_description="Adds a new patient or associates an existing one with the logged-in doctor.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'pesel': openapi.Schema(type=openapi.TYPE_STRING, description='PESEL number of the patient'),
                'date_of_birth': openapi.Schema(type=openapi.TYPE_STRING, description='Date of birth of the patient'),
                'date_of_diagnosis': openapi.Schema(type=openapi.TYPE_STRING,
                                                    description='Date of diagnosis (optional)'),
                'sex': openapi.Schema(type=openapi.TYPE_STRING, description='Sex of the patient (M/F)'),
                'other_fields': openapi.Schema(type=openapi.TYPE_STRING, description='Additional fields as required'),
            },
            required=['pesel', 'date_of_birth', 'sex']
        ),
        responses={
            201: 'Patient added successfully',
            400: 'Bad Request'
        }
    )
    def post(self, request):
        """
               POST method to add a new patient or associate an existing patient with the logged-in doctor.

               This method checks if the patient already exists in the database based on 'pesel' (PESEL number).
               If the patient exists, it associates the patient with the doctor.
               If the patient does not exist, it creates a new patient profile and associates it with the doctor.

               Returns:
                   - 201 Created: Patient successfully added or associated.
                   - 400 Bad Request: Errors in input data or unauthorized access.

               Possible Errors:
                   - If user is not logged in or session has expired, returns 401 Unauthorized.
                   - If the doctor is not authorized (not logged in as a doctor), returns 400 Bad Request.
                   - If the patient is already associated with the doctor, returns 400 Bad Request.
               """
        role_vale = Role['PATIENT'].value
        pesel = request.data.get('pesel')

        try:
            # Get user_id from session
            user_id = request.session.get('user_id')

            doctor = Doctor.objects.get(user_id_id=user_id)
            print(doctor)
            doctor_id = doctor.id
        except Doctor.DoesNotExist:
            return Response({'error': 'User is not logged in or session has expired'},
                            status=status.HTTP_401_UNAUTHORIZED)

        if UserProfile.objects.filter(pesel=pesel).exists():
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
            doctor_user_id = Doctor.objects.get(id=doctor_id).user_id

            if user_profile_serializer.is_valid() and Auth.objects.get(id=doctor_user_id).role == Role['DOCTOR'].value:
                user_profile = user_profile_serializer.save()

                auth_data = {
                    'login': None,
                    'password': None,
                    'role': role_vale,
                    'id': user_profile.id
                }

                patient_data = {
                    'date_of_birth': request.data['date_of_birth'],
                    'date_of_diagnosis': request.data.get('date_of_diagnosis', None),
                    'sex': Sex[request.data['sex']].value,
                    'user_id': user_profile.id
                }

                auth_serializer = AuthSerializer(data=auth_data)
                patient_serializer = PatientSerializer(data=patient_data)

                if patient_serializer.is_valid() and Auth.objects.get(id=doctor_user_id).role == Role['DOCTOR'].value:

                    patient_serializer.save()

                    patient_and_doctor_data = {
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
    @swagger_auto_schema(
        operation_description="Updates authentication information for an existing patient.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'pesel': openapi.Schema(type=openapi.TYPE_STRING, description='PESEL number of the patient'),
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='Name of the patient'),
                'surname': openapi.Schema(type=openapi.TYPE_STRING, description='Surname of the patient'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email address of the patient'),
                'login': openapi.Schema(type=openapi.TYPE_STRING, description='New login for authentication'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='New password for authentication'),
            },
            required=['pesel', 'name', 'surname', 'email', 'login', 'password']
        ),
        responses={
            200: 'Authentication information updated successfully',
            400: 'Bad Request'
        }
    )
    def patch(self, request):
        """
            Patch API endpoint to update authentication information for an existing patient.

            This endpoint allows an existing patient to update their authentication information,
            including login and password, by verifying their PESEL number and other personal details.
            """

        request.data['role'] = 'PATIENT'
        role_value = Role[request.data['role']].value
        pesel = request.data['pesel']
        name = request.data['name']
        surname = request.data['surname']
        email = request.data['email']

        login_new = request.data['login']
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

                    request.session['user_role'] = 'PATIENT'
                    request.session['user_id'] = user_id
                    request.session.modified = True
                    request.session.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response({"error": ""}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'User profile data does not match.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('The patient with a given PESEL number is not in the database',
                            status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    @swagger_auto_schema(
        operation_description="Updates authentication information for an existing patient.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'pesel': openapi.Schema(type=openapi.TYPE_STRING, description='PESEL number of the patient'),
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='Name of the patient'),
                'surname': openapi.Schema(type=openapi.TYPE_STRING, description='Surname of the patient'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email address of the patient'),
                'login': openapi.Schema(type=openapi.TYPE_STRING, description='New login for authentication'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='New password for authentication'),
            },
            required=['pesel', 'name', 'surname', 'email', 'login', 'password']
        ),
        responses={
            200: 'Authentication information updated successfully',
            400: 'Bad Request'
        }
    )
    def post(self, request):
        """
                PATCH method to update authentication information for an existing patient.

                This method verifies if the patient exists in the database based on 'pesel' (PESEL number).
                It checks if the provided profile data (name, surname, email) matches the existing profile.
                If valid, it updates the login and password for authentication using AuthUpdateSerializer.

                Returns:
                    - 200 OK: Authentication information updated successfully.
                    - 400 Bad Request: Errors in input data, mismatch in profile data, or patient not found.

                Possible Errors:
                    - If the patient with the provided PESEL number is not found, returns 400 Bad Request.
                    - If the provided profile data (name, surname, email) does not match the existing profile, returns 400 Bad Request.
                """
        print(request)

        login_value = request.data.get('login')
        password = request.data.get('password')
        auth_backend = AuthBackend()
        user = auth_backend.authenticate(request, login=login_value, password=password)

        if user is not None:
            request.session['user_role'] = user.role
            request.session['user_id'] = user.id_id
            request.session.modified = True
            request.session.save()
            return Response({'message': 'User logged in', 'role': user.role, 'user_id': user.id_id},
                            status=status.HTTP_200_OK)
        else:

            return Response('Nieprawidłowe dane logowania', status=400)

def generate_frames():
    """
            GET method to retrieve the role of a user by their login username.

            This method expects a 'login' parameter in the query string to identify the user.
            It queries the Auth model to find a user with the specified login username.
            If found, it returns the role of the user as JSON response.
            If not found, it returns an error message with status code 404.

            Returns:
                - 200 OK: Returns JSON with the user's role.
                - 404 Not Found: If no user is found with the provided login.

            Example:
                GET /api/user-role/?login=johndoe

            Response:
                {
                    'role': 'ADMIN'
                }
            """
    processor = VideoProcessor()  # call VideoProcessor class from AI model
    while True:
        frame = processor.process_frame()
        if frame is None:
            break
        yield (b'--frame\r\n'  # returns the processed frame as a byte string
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@api_view(['POST'])
@swagger_auto_schema(
        operation_description="Capture and process a photo, saving it as a reference photo for a patient.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'image': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_BINARY,
                                        description='Base64-encoded image data')
            },
            required=['image']
        ),
        responses={
            201: 'Created',
            400: 'Bad Request'
        }
    )
def capture_photo(request):
    """
       Endpoint to capture and process a photo from request data.

       Args:
           request (HttpRequest): The HTTP request object containing image data.

       Returns:
           Response: HTTP response indicating success or failure of photo capture
                     and processing.

       Raises:
           Patient.DoesNotExist: If the patient corresponding to the user_id
                                  from session does not exist.

       Note:
           This function captures an image from the request, decodes it,
           associates it with a patient, processes landmarks, and saves
           the reference photo and its landmarks in the database.
       """

    data = request.data
    image_data = data['image']
    image_data = base64.b64decode(image_data.split(',')[1])
    np_arr = np.frombuffer(image_data, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    date_now = datetime.now().isoformat() + "Z"

    user_id = request.session.get('user_id')

    patient = Patient.objects.get(user_id_id=user_id)  # tutaj jest problem

    patient_id = patient.id

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
        ref_photo_instance = ref_photos_serializer.save()

        for landmark, distance in distances.items():
            ref_photo_landmarks_data = {
                'distance': distance,
                'landmark_number': landmark,
                'ref_photo': ref_photo_instance.id
            }
            ref_photos_landmarks_serializer = RefPhotoLandmarksSerializer(data=ref_photo_landmarks_data)
            if ref_photos_landmarks_serializer.is_valid():
                ref_photos_landmarks_serializer.save()
            else:
                # Obsłuż błędy walidacji
                return Response(ref_photos_landmarks_serializer.errors, status=400)

        return Response(ref_photos_serializer.data, status=201)
    else:
        return Response(ref_photos_serializer.errors, status=400)


@api_view(['GET'])  # streams the video frames to the client
def video_stream(request):
    return StreamingHttpResponse(generate_frames(), content_type='multipart/x-mixed-replace; boundary=frame')


@swagger_auto_schema(
    method='get',
    operation_description="Starts the video processing and returns a confirmation message.",
    responses={200: openapi.Response(description="Video processing started.")}
)
@api_view(['GET'])  # just a message that recoding has started
def start_video_processing(request):
    """
        GET API endpoint to start video processing.

        This endpoint starts the video processing task and returns a confirmation message
        to the client indicating that video processing has started.
        """
    return HttpResponse("Video processing started.")


@swagger_auto_schema(
    method='post',
    operation_description="Adds a new video recording and processes it to extract frame and landmark information.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'video': openapi.Schema(type=openapi.TYPE_FILE, description='Video file for processing'),
        },
        required=['video']
    ),
    responses={
        201: openapi.Response(description='Recording added and processed successfully.'),
        400: openapi.Response(description='Bad Request.'),
        404: openapi.Response(description='Patient not found.'),
    }
)
@api_view(['POST'])
def add_recording(request):
    """
        POST API endpoint to add a new video recording and process it.

        This endpoint accepts a video file, processes it to extract frame and landmark information,
        and stores the results in the database. It also generates a report based on the differences
        between current frame landmarks and reference photo landmarks.
        """
    global frame_id
    user_id = request.session.get('user_id')

    try:
        patient = Patient.objects.get(user_id_id=user_id)  # Pobierz instancję pacjenta
    except Patient.DoesNotExist:
        return Response({'error': 'Patient not found'}, status=status.HTTP_404_NOT_FOUND)

    video_file = request.FILES.get('video')
    if not video_file:
        return Response({'error': 'No video file provided'}, status=status.HTTP_400_BAD_REQUEST)

    file_path = default_storage.save('temp/recording.webm', video_file)
    processor = VideoProcessor()
    all_frames_data, frame_number_with_max_distance, landmark_list = processor.process_video(file_path)
    date_now = datetime.now().isoformat() + "Z"

    recording_data = {
        'date': date_now,
        'time': 10,
        'patient_id': patient.user_id.id,  # Użyj identyfikatora user_id
    }

    recordings_serializer = RecordingsSerializer(data=recording_data)
    if recordings_serializer.is_valid():
        recording = recordings_serializer.save()

        frame_data = all_frames_data.get(frame_number_with_max_distance)
        if frame_data:
            frame_serializer = FramesSerializer(data={
                'recording_id': recording.id,
                'frame_number': frame_number_with_max_distance,
                'timestamp': frame_data['timestamp'],
                'x_center': frame_data.get('x_center', 0),
                'y_center': frame_data.get('y_center', 0),
            })
            if frame_serializer.is_valid():
                frame = frame_serializer.save()
                frame_id = frame.id
                for landmark_index, distance in frame_data['landmarks'].items():
                    landmark_serializer = FrameLandmarksSerializer(data={
                        'frame_id': frame.id,
                        'landmark_number': landmark_index,
                        'distance': distance,
                    })
                    if landmark_serializer.is_valid():
                        landmark_serializer.save()
                    else:
                        return Response(landmark_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        current_frame_landmarks = FrameLandmarks.objects.filter(frame_id=frame_id)
        ref_photo_id = RefPhotos.objects.filter(patient_id_id=patient.id).order_by('-date').first().id

        current_distances = {landmark.landmark_number: landmark.distance for landmark in current_frame_landmarks}

        ref_landmarks = RefPhotoLandmarks.objects.filter(ref_photo=ref_photo_id)
        ref_distances = {landmark.landmark_number: landmark.distance for landmark in ref_landmarks}
        date_now = datetime.now().isoformat() + "Z"
        differences = {}
        for landmark in ref_distances.keys():
            if landmark in current_distances:
                differences[landmark] = abs(ref_distances[landmark] - current_distances[landmark])

        report_data = {
            'patient_id': patient.id,
            'date': date_now,
            'difference_mouth': differences.get(61, 0),  # Assuming 61 is a landmark for the mouth
            'difference_2': differences.get(291, 0),  # Assuming 291 is another critical landmark
        }
        report_serializer = ReportsSerializer(data=report_data)
        if report_serializer.is_valid():
            report_serializer.save()

        return Response(recordings_serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(recordings_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def calculate_difference(landmark_list, patient_id):
    """
        Calculate the differences between the current and reference distances for mouth and eyebrow landmarks.

        Args:
            landmark_list (list): List of tuples representing the landmark points. Each tuple contains three elements.
            patient_id (int): The ID of the patient.

        Returns:
            tuple: A tuple containing the differences for mouth and eyebrow landmarks (mouth_diff, eyebrow_diff).

        Raises:
            ValueError: If the landmark_list is not a list of tuples or if the ref_landmarks is not in the expected format.
        """
    processor = VideoProcessor()

    # Upewnij się, że landmark_list jest listą krotek
    if not isinstance(landmark_list, list) or not all(
            isinstance(point, tuple) and len(point) == 3 for point in landmark_list):
        raise ValueError(
            f"Oczekiwana lista krotek punktów orientacyjnych, otrzymano {type(landmark_list)} w niepoprawnym formacie")

    # Obliczanie bieżących odległości
    current_mouth = processor.calculate_distance_mouth(landmark_list)
    current_eyebrow = (processor.calculate_distance(landmark_list)[55] +
                       processor.calculate_distance(landmark_list)[285]) / 2

    # Pobierz odległości referencyjne
    ref_landmarks = services.get_ref_distances_for_landmarks(patient_id, [55, 285, 61, 291])

    # Debugowanie, aby zrozumieć format ref_landmarks
    print(f"ref_landmarks: {ref_landmarks}")

    # Upewnij się, że ref_landmarks jest słownikiem, gdzie klucze to indeksy punktów orientacyjnych, a wartościami są liczby
    if not isinstance(ref_landmarks, dict) or not all(
            isinstance(k, int) and isinstance(v, (float, int)) for k, v in ref_landmarks.items()):
        raise ValueError(
            f"Oczekiwany słownik punktów orientacyjnych, otrzymano {type(ref_landmarks)} w niepoprawnym formacie")

    # Obliczanie odległości referencyjnych bez dodatkowego przetwarzania
    ref_mouth = ref_landmarks[61]
    ref_eyebrow = (ref_landmarks[55] + ref_landmarks[285]) / 2

    # Obliczanie różnic
    eyebrow_diff = current_eyebrow - ref_eyebrow
    mouth_diff = current_mouth - ref_mouth

    return mouth_diff, eyebrow_diff

@swagger_auto_schema(
    method='delete',
    operation_description="Deletes a user and their associated data.",
    responses={
        200: openapi.Response(description='User deleted successfully.'),
        500: openapi.Response(description='Failed to delete user.')
    }
)
@api_view(['DELETE'])  # not used
def delete_user(request, user_id):
    """
        DELETE API endpoint to delete a user and their associated data.

        This endpoint deletes a user from the Auth table and also removes associated data
        if the user is a patient or a doctor.
        """
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

        UserProfile.objects.filter(id=user_id).delete()
        return Response({'message': 'User deleted successfully'}, status=200)

    except Exception as e:
        # Obsługa wyjątku (np. gdy wystąpi problem z bazą danych)
        return Response({'error': 'Failed to delete user', 'details': str(e)}, status=500)

@swagger_auto_schema(
    method='delete',
    operation_description="Deletes a patient and their associated data by patient ID.",
    responses={
        200: openapi.Response(description='Patient deleted successfully.'),
        404: openapi.Response(description='Patient not found.'),
        500: openapi.Response(description='Failed to delete patient.')
    }
)
@api_view(['DELETE'])  # for admin
def delete_patient(request, patient_id):
    """
        DELETE API endpoint to delete a patient and their associated data.

        This endpoint is intended for administrative use to delete a patient and their associated
        data including authentication, user profile, and patient-doctor assignments.
        """
    try:
        patient = Patient.objects.filter(id=patient_id).first()
        if patient:

            user_id = patient.user_id_id
            Auth.objects.filter(id=user_id).delete()
            patient.delete()
            DoctorAndPatient.objects.filter(patient_id=patient_id).delete()
            UserProfile.objects.filter(id=user_id).delete()

            return Response({'message': 'Patient deleted successfully'}, status=200)

        else:
            return Response({'error': 'Patient not found'}, status=404)

    except Exception as e:
        # Handle exception (e.g., database issue)
        return Response({'error': 'Failed to delete patient', 'details': str(e)}, status=500)

@swagger_auto_schema(
    method='get',
    operation_description="Fetches patients associated with the logged-in doctor.",
    responses={
        200: openapi.Response(description='List of patients fetched successfully.'),
        401: openapi.Response(description='User is not logged in or session has expired.'),
        404: openapi.Response(description='No doctor found for this user.'),
        400: openapi.Response(description='Bad request.'),
    }
)
@api_view(['GET'])
def get_patients_by_doctor(request):
    """
       GET API endpoint to fetch patients associated with the logged-in doctor.

       This endpoint retrieves the list of patients that are associated with the currently logged-in doctor.
       """
    try:
        # Get user_id from session
        user_id = request.session.get('user_id')
        if not user_id:
            return Response({'error': 'User is not logged in or session has expired'},
                            status=status.HTTP_401_UNAUTHORIZED)

        try:
            doctor = Doctor.objects.get(user_id=user_id)
        except Doctor.DoesNotExist:
            return Response({'error': 'No doctor found for this user'}, status=status.HTTP_404_NOT_FOUND)

        doctor_id = doctor.id
        doctor_patient_relations = DoctorAndPatient.objects.filter(doctor_id=doctor_id)
        patient_ids = doctor_patient_relations.values_list('patient_id', flat=True)

        patients = Patient.objects.filter(id__in=patient_ids).select_related('user_id')

        serializer = PatientSerializer1(patients, many=True)

        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='get',
    operation_description="Fetches reports for a specific patient associated with the logged-in doctor.",
    responses={
        200: openapi.Response(description='List of reports fetched successfully.'),
        401: openapi.Response(description='User is not logged in or session has expired.'),
        404: openapi.Response(description='No doctor found for this user or no reports found for the patient.'),
        400: openapi.Response(description='Bad request.'),
    }
)

@api_view(['GET'])
def get_reports_for_doctor_view(request, patient_id):
    """
        GET API endpoint to fetch reports for a specific patient associated with the logged-in doctor.

        This endpoint retrieves the list of reports for a patient associated with the currently logged-in doctor.
        """
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
            return Response(serializer.data, status=status.HTTP_200_OK)


    except Reports.DoesNotExist:
        return Response({'error': 'No reports found for this patient'}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='get',
    operation_description="Fetches details of the patient associated with the logged-in doctor.",
    responses={
        200: openapi.Response(description='Patient details fetched successfully.'),
        401: openapi.Response(description='User is not logged in or session has expired.'),
        400: openapi.Response(description='Bad request.'),
    }
)
@api_view(['GET'])
def patient_details_view(request):
    """
        GET API endpoint to fetch details of the patient associated with the logged-in doctor.

        This endpoint retrieves and returns details of the patient associated with the currently logged-in doctor.
        """
    user_doctor_id = request.session.get('user_id')
    details = get_patient_details(request)
    return Response(details, status=200)

@swagger_auto_schema(
    method='get',
    operation_description="Fetches reports for the logged-in patient.",
    responses={
        200: openapi.Response(description='List of reports fetched successfully.'),
        401: openapi.Response(description='User is not logged in or session has expired.'),
        404: openapi.Response(description='No patient found for this user or no reports found for the patient.'),
        400: openapi.Response(description='Bad request.'),
    }
)
@api_view(['GET'])
def get_reports_for_patient_view(request):
    """
       GET API endpoint to fetch reports for the logged-in patient.

       This endpoint retrieves the list of reports for the patient associated with the currently logged-in user.
       """
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
        return Response(serializer.data, status=status.HTTP_200_OK)


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
        serializer = PatientsSerializer(patients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CreateReportView(APIView):
    def post(self, request):
        try:
            # Generate the report
            user_id = request.session.get('user_id')
            patient_id = Patient.objects.get(user_id=user_id).id

            today = date.today()
            patient_data = get_patient_details(patient_id)
            file_name = patient_data["name"] + "report" + str(today) + ".pdf"
            x = create_report(patient_id)

            # Path to the generated PDF
            file_path = os.path.join(os.getcwd(), x)
            return Response({'error': 'dziala'}, status=status.HTTP_200_OK)
            # Return the PDF file as a response

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class CreateReportViewDOC(APIView):
    def post(self, request):
        try:
            patient_id = request.data.get('patient_id')

            if not patient_id:
                return Response({'error': 'Patient ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

            # Generate the report
            today = date.today()
            patient_data = services.get_patient_details(patient_id)

            file_name = f"{patient_data['name']}report{today}.pdf"
            x = create_report(patient_id)

            # Path to the generated PDF
            file_path = os.path.join(os.getcwd(), x)

            # Return a success message or the file
            if os.path.exists(file_path):
                return Response({'message': 'Report generated successfully.'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Report generation failed.'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            return Response({'error dziala': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

