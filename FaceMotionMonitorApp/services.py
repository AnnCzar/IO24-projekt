from django.db.models import Max
from FaceMotionMonitorApp.models.userProfile_models import (
    Recordings, Frames, FrameLandmarks, RefPhotoLandmarks,
    RefPhotos, Auth, Doctor, DoctorAndPatient, Patient,
    UserProfile, Reports
)
from FaceMotionMonitorApp.serializers import (
    ReportsSerializer, PatientSerializer, AuthUpdateSerializer,
    DoctorAndPatientSerializer, DoctorSerializer, AuthSerializer,
    UserProfileSerializer
)


def create_user_profile(data):
    """
    Create a user profile.

    Args:
        data (dict): The data for the user profile.

    Returns:
        UserProfile: The created user profile instance.
        dict: The errors if the serializer is not valid.
    """
    user_profile_serializer = UserProfileSerializer(data=data)
    if user_profile_serializer.is_valid():
        return user_profile_serializer.save()
    return None, user_profile_serializer.errors


def create_auth(auth_data):
    """
    Create an auth entry.

    Args:
        auth_data (dict): The data for the auth entry.

    Returns:
        Auth: The created auth instance.
        dict: The errors if the serializer is not valid.
    """
    auth_serializer = AuthSerializer(data=auth_data)
    if auth_serializer.is_valid():
        return auth_serializer.save()
    return None, auth_serializer.errors


def create_doctor(doctor_data):
    """
    Create a doctor entry.

    Args:
        doctor_data (dict): The data for the doctor.

    Returns:
        Doctor: The created doctor instance.
        dict: The errors if the serializer is not valid.
    """
    doctor_serializer = DoctorSerializer(data=doctor_data)
    if doctor_serializer.is_valid():
        return doctor_serializer.save()
    return None, doctor_serializer.errors


def add_patient_to_doctor(patient_id, doctor_id):
    """
    Link a patient to a doctor.

    Args:
        patient_id (int): The ID of the patient.
        doctor_id (int): The ID of the doctor.

    Returns:
        DoctorAndPatient: The created relationship instance.
        dict: The errors if the serializer is not valid.
    """
    patient_and_doctor_data = {
        'patient_id': patient_id,
        'doctor_id': doctor_id
    }
    patient_doctor_serializer = DoctorAndPatientSerializer(data=patient_and_doctor_data)
    if patient_doctor_serializer.is_valid():
        return patient_doctor_serializer.save()
    return None, patient_doctor_serializer.errors


def update_auth(user, new_data):
    """
    Update authentication data.

    Args:
        user (Auth): The user instance to update.
        new_data (dict): The new data for the user.

    Returns:
        Auth: The updated user instance.
        dict: The errors if the serializer is not valid.
    """
    serializer = AuthUpdateSerializer(user, data=new_data)
    if serializer.is_valid():
        return serializer.save()
    return None, serializer.errors


def delete_user(user_id):
    """
    Delete a user and related entries.

    Args:
        user_id (int): The ID of the user to delete.

    Returns:
        dict: Success message or error details.
        int: HTTP status code.
    """
    try:
        Auth.objects.filter(id=user_id).delete()
        patient = Patient.objects.filter(user_id=user_id).first()
        if patient:
            patient_id = patient.id
            patient.delete()
            DoctorAndPatient.objects.filter(patient_id=patient_id).delete()

        doctor = Doctor.objects.filter(user_id=user_id).first()
        if doctor:
            doctor_id = doctor.id
            doctor.delete()
            DoctorAndPatient.objects.filter(doctor_id=doctor_id).delete()

        UserProfile.objects.filter(id=user_id).delete()
        return {'message': 'User deleted successfully'}, 200
    except Exception as e:
        return {'error': 'Failed to delete user', 'details': str(e)}, 500


def get_patients_by_doctor(user_id):
    """
    Get patients by doctor ID.

    Args:
        user_id (int): The user ID of the doctor.

    Returns:
        list: Serialized patient data.
        str: Error message if any.
    """
    try:
        doctor = Doctor.objects.get(user_id=user_id)
        doctor_id = doctor.id
        doctor_patient_relations = DoctorAndPatient.objects.filter(doctor_id=doctor_id)
        patient_ids = doctor_patient_relations.values_list('patient_id', flat=True)
        patients = Patient.objects.filter(id__in=patient_ids).select_related('user_id')
        serializer = PatientSerializer(patients, many=True)
        return serializer.data, None
    except Exception as e:
        return None, str(e)


def get_reports_for_doctor(doctor_id, patient_id):
    """
    Get reports for a doctor by doctor ID and patient ID.

    Args:
        doctor_id (int): The ID of the doctor.
        patient_id (int): The ID of the patient.

    Returns:
        list: Serialized report data.
        str: Error message if any.
    """
    if DoctorAndPatient.objects.filter(doctor_id=doctor_id, patient_id=patient_id).exists():
        reports = Reports.objects.filter(patient_id=patient_id)
        serializer = ReportsSerializer(reports, many=True)
        return serializer.data, None
    return None, 'No reports found for this patient'


def calculate_difference(landmarks_data):
    """
    Calculate differences between landmarks.

    Args:
        landmarks_data (list): A list of landmark data.

    Returns:
        tuple: Differences for mouth and eyebrow.
    """
    distances = [data['distance'] for data in landmarks_data]
    mouth_diff = 0
    eyebrow_diff = 0
    return mouth_diff, eyebrow_diff


def get_reports_for_patient(patient_id):
    """
    Get reports for a patient by patient ID.

    Args:
        patient_id (int): The ID of the patient.

    Returns:
        list: Serialized report data.
        str: Error message if any.
    """
    reports = Reports.objects.filter(patient_id=patient_id)
    serializer = ReportsSerializer(reports, many=True)
    return serializer.data, None


def get_max_landmark_distance(patient_id, landmark_number):
    """
    Get the maximum landmark distance for a patient by patient ID and landmark number.

    Args:
        patient_id (int): The ID of the patient.
        landmark_number (int): The landmark number.

    Returns:
        dict: The maximum distance for the specified landmark.
    """
    try:
        latest_recording = Recordings.objects.filter(patient_id=patient_id).latest('date')
        frames = Frames.objects.filter(recording_id=latest_recording)
        max_distance = FrameLandmarks.objects.filter(frame_id__in=frames, landmark_number=landmark_number).aggregate(
            Max('distance')
        )
        return max_distance
    except Recordings.DoesNotExist:
        return None  # Handle case where no recordings exist for the patient
    except Frames.DoesNotExist:
        return None  # Handle case where no frames exist for the recording
    except FrameLandmarks.DoesNotExist:
        return None  # Handle case where no landmarks exist for the frames


def get_patients_for_doctor(doctor_id):
    """
    Get patients for a doctor by doctor ID.

    Args:
        doctor_id (int): The ID of the doctor.

    Returns:
        dict: A dictionary with patient data and user data.
    """
    try:
        doctor_patients = DoctorAndPatient.objects.filter(doctor_id=doctor_id)
        patient_ids = [dp.patient_id for dp in doctor_patients]
        patients = Patient.objects.filter(id__in=patient_ids)
        users = UserProfile.objects.filter(id__in=[patient.user_id_id for patient in patients])
        patient_data = {}
        for patient in patients:
            patient_data[patient.id] = {
                'patient_data': patient,
                'user_data': next((user for user in users if user.id == patient.user_id_id), None)
            }
        return patient_data
    except Exception as e:
        print(f"Error occurred: {e}")
        return {}


def get_patient_details(patient_id):
    """
    Get patient details for reports by patient ID.

    Args:
        patient_id (int): The ID of the patient.

    Returns:
        dict: A dictionary with patient details.
    """
    patient = Patient.objects.get(id=patient_id)
    user_profile = UserProfile.objects.get(id=patient.user_id_id)
    patient_details = {
        'name': user_profile.name,
        'surname': user_profile.surname,
        'pesel': user_profile.pesel,
        'date_of_birth': patient.date_of_birth,
        'date_of_diagnosis': patient.date_of_diagnosis,
    }
    return patient_details


def get_ref_distances_for_landmarks(patient_id, landmark_numbers):
    """
    Get reference distances for landmarks by patient ID and landmark numbers.

    Args:
        patient_id (int): The ID of the patient.
        landmark_numbers (list): A list of landmark numbers.

    Returns:
        dict: A dictionary with distances for selected landmarks.
    """
    try:
        landmarks = RefPhotoLandmarks.objects.filter(ref_photo__patient_id_id=patient_id,
                                                     landmark_number__in=landmark_numbers)
        distances = {}
        for landmark in landmarks:
            distances[landmark.landmark_number] = landmark.distance
        return distances
    except Exception as e:
        print(f"Error occurred: {e}")
        return {}


def get_centers_for_patient(patient_id):
    """
    Get centers for patient by patient ID.

    Args:
        patient_id (int): The ID of the patient.

    Returns:
        list: A list of tuples with x_center and y_center.
    """
    try:
        photos = RefPhotos.objects.filter(patient_id_id=patient_id)
        centers = [(photo.x_center, photo.y_center) for photo in photos]
        return centers
    except Exception as e:
        print(f"Error occurred: {e}")
        return []


def get_users_with_roles():
    """
    Get users with roles.

    Returns:
        list: A list of tuples with user and their role.
    """
    try:
        users = UserProfile.objects.all()
        users_with_roles = []
        for user in users:
            auth_data = Auth.objects.filter(id=user.id).first()
            role = auth_data.role if auth_data else None
            users_with_roles.append((user, role))
        return users_with_roles
    except Exception as e:
        print(f"Error occurred: {e}")
        return []


def get_landmarks_for_patient(patient_id):
    """
    Get landmarks for a patient by patient ID.

    Args:
        patient_id (int): The ID of the patient.

    Returns:
        list: A list of distances for specified landmarks.
    """
    landmark_numbers = [61, 291, 55, 285]
    try:
        ref_photos = RefPhotos.objects.filter(patient_id__id=patient_id)
        distances = RefPhotoLandmarks.objects.filter(
            ref_photo__in=ref_photos,
            landmark_number__in=landmark_numbers
        ).values_list('distance', flat=True)
        return list(distances)
    except Exception as e:
        print(f"Error: {e}")
        return None


def get_data_for_reports(patient_id):
    """
    Get data for reports by patient ID.

    Args:
        patient_id (int): The ID of the patient.

    Returns:
        tuple: Lists of dates, mouth differences, and second differences.
    """
    try:
        reports = Reports.objects.filter(patient_id_id=patient_id)
        dates = [report.date for report in reports]
        differences_mouth = [report.difference_mouth for report in reports]
        differences_2 = [report.difference_2 for report in reports]
        return dates, differences_mouth, differences_2
    except Exception as e:
        print(f"Error: {e}")
        return [], [], []
