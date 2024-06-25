"""
URL configuration for FaceMotionMonitor project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.views.generic import TemplateView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from FaceMotionMonitorApp.views import DoctorRegistration, LoginView, AddPatient, PatientRegistration, \
    video_stream, start_video_processing, capture_photo, \
    delete_user, get_patients_by_doctor, get_reports_for_doctor_view, patient_details_view, \
    get_reports_for_patient_view, CreateReportView, CreateReportViewDOC, LogoutView, delete_patient, get_all_patients, add_recording
schema_view = get_schema_view(
   openapi.Info(
      title="API Documentation",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@local.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)





urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', DoctorRegistration.as_view(), name='register-doctor'),
    path('addPatient/', AddPatient.as_view(), name='add-patient'),
    path('registerPatient/', PatientRegistration.as_view(), name='register-patient'),
    path('login/', LoginView.as_view(), name='login'),
    path('video-stream/', video_stream, name='video_stream'),
    path('start-video-processing/', start_video_processing, name='start_video_processing'),
    path('capture-photo/', capture_photo, name='capture_photo'),  # capture the photo
    path('delete-user/<int:user_id>/', delete_user, name='delete_user'),
    path('patients/by-doctor/', get_patients_by_doctor, name='get_patients_by_doctor'),
    path('reports/doctor/<int:patient_id>/', get_reports_for_doctor_view, name='get_reports_for_doctor'),
    path('patient/details/', patient_details_view, name='patient_details'),
    path('reports/patient/', get_reports_for_patient_view, name='get_reports_for_patient'),
    path('delete_patient/<int:patient_id>/', delete_patient, name='delete_patient'),
    path('patients/', get_all_patients, name='get_all_patients'),
    path('add_recording/', add_recording, name='add_recording'),
    path('logout/', LogoutView.as_view(), name='logout'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('create-report/', CreateReportView.as_view(), name='create-report'),
    path('create-report_doc/', CreateReportViewDOC.as_view(), name='create-reportDOC'),

    path('', TemplateView.as_view(template_name='index.html')),

]