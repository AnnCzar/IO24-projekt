from django.db.models import Max
from django.utils import timezone

from FaceMotionMonitorApp.models.userProfile_models import Recordings, Frames, FrameLandmarks, RefPhotoLandmarks, RefPhotos, UserProfile, Auth



def get_max_landmark_distance(patient_id, landmark_number):
    try:
        # Get the latest recording for the given patient
        latest_recording = Recordings.objects.filter(patient_id=patient_id).latest('date')

        # Get the frames associated with the latest recording
        frames = Frames.objects.filter(recording_id=latest_recording)

        # Get the maximum distance for the specified landmark number
        max_distance = FrameLandmarks.objects.filter(frame_id__in=frames, landmark_number=landmark_number).aggregate(Max('distance'))

        return max_distance
    except Recordings.DoesNotExist:
        return None  # Handle case where no recordings exist for the patient
    except Frames.DoesNotExist:
        return None  # Handle case where no frames exist for the recording
    except FrameLandmarks.DoesNotExist:
        return None  # Handle case where no landmarks exist for the frames

# Example usage
# patient_id = 1  # Replace with actual patient ID
# landmark_number = 2  # Replace with the desired landmark number
# max_distance = get_max_landmark_distance(patient_id, landmark_number)


from FaceMotionMonitorApp.models.userProfile_models import DoctorAndPatient, Patient, UserProfile, Reports

def get_patients_for_doctor(doctor_id):
    try:
        # Pobranie rekordów z tabeli DoctorAndPatient dla danego doktora
        doctor_patients = DoctorAndPatient.objects.filter(doctor_id=doctor_id)

        # Pobranie identyfikatorów pacjentów przypisanych do danego doktora
        patient_ids = [dp.patient_id for dp in doctor_patients]

        # Pobranie danych pacjentów na podstawie ich identyfikatorów
        patients = Patient.objects.filter(id__in=patient_ids)

        # Pobranie danych użytkowników dla pacjentów
        users = UserProfile.objects.filter(id__in=[patient.user_id_id for patient in patients])

        # Stworzenie słownika, gdzie klucz to ID pacjenta, a wartość to dane pacjenta i użytkownika
        patient_data = {}
        for patient in patients:
            patient_data[patient.id] = {
                'patient_data': patient,
                'user_data': next((user for user in users if user.id == patient.user_id_id), None)
            }

        # Zwrócenie słownika
        return patient_data
    except Exception as e:
        # Obsługa wyjątku (np. gdy nie ma pacjentów przypisanych do danego doktora)
        print(f"Error occurred: {e}")
        return {}

#EXAMPLE
# patients_data = get_patients_for_doctor(doctor_id)
#
# # Wyświetlenie danych pacjentów
# for patient_id, data in patients_data.items():
#     print("Patient ID:", patient_id)
#     print("Patient Data:", data['patient_data'])
#     print("User Data:", data['user_data'])
#     print("\n")



def get_reports_for_patient(patient_id):
    try:
        # Pobranie wszystkich raportów dla danego pacjenta
        reports = Reports.objects.filter(patient_id_id=patient_id)

        # Zwrócenie raportów
        return reports
    except Exception as e:
        # Obsługa wyjątku (np. gdy nie ma raportów dla danego pacjenta)
        print(f"Error occurred: {e}")
        return []


#EXAMPLE
# reports = get_reports_for_patient(patient_id)
#
# # Wyświetlenie danych raportów
# for report in reports:
#     print("Report ID:", report.id)
#     print("Date:", report.date)
#     print("Difference Mouth:", report.difference_mouth)
#     print("Difference 2:", report.difference_2)
#     print("\n")


def get_ref_distances_for_landmarks(patient_id, landmark_numbers):
    try:
        # Pobranie wszystkich landmarków dla danego pacjenta
        landmarks = RefPhotoLandmarks.objects.filter(ref_photo__patient_id_id=patient_id, landmark_number__in=landmark_numbers)

        # Stworzenie słownika, gdzie kluczem będzie numer landmarku, a wartością dystans dla tego landmarku
        distances = {}
        for landmark in landmarks:
            distances[landmark.landmark_number] = landmark.distance

        # Zwrócenie słownika z dystansami dla wybranych landmarków
        return distances
    except Exception as e:
        # Obsługa wyjątku (np. gdy nie ma danych dla danego pacjenta lub landmarków)
        print(f"Error occurred: {e}")
        return {}


#EXAMPLE
# patient_id = 1
# landmark_numbers = [1, 2, 3]
# distances = get_ref_distances_for_landmarks(patient_id, landmark_numbers)
# for landmark_number, distance in distances.items():
#     print(f"Landmark {landmark_number}: Distance = {distance}")



def get_centers_for_patient(patient_id):
    try:
        photos = RefPhotos.objects.filter(patient_id_id=patient_id)
        centers = [(photo.x_center, photo.y_center) for photo in photos]
        # Zwrócenie listy krotek z współrzędnymi x_center i y_center dla zdjęć referencyjnych
        return centers
    except Exception as e:
        print(f"Error occurred: {e}")
        return []


#for admin
def get_users_with_roles():
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


#EXAMPLE
# users_with_roles = get_users_with_roles()
#
# for user, role in users_with_roles:
#     print("Name:", user.name)
#     print("Surname:", user.surname)
#     print("Email:", user.email)
#     print("PESEL:", user.pesel)
#     print("Role:", role)
#     print("\n")
