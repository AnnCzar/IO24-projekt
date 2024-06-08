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
from django.urls import path
from django.views.generic import TemplateView

from FaceMotionMonitorApp.views import DoctorRegistration, LoginView, AddPatient, PatientRegistration, \
    video_stream, start_video_processing, AddRecordingView, AddFrameView, AddFrameLandmarksView, CapturePhotoView, \
    delete_user

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', DoctorRegistration.as_view(), name='register-doctor'),
    path('addPatient/', AddPatient.as_view(), name='add-patient'),
    path('registerPatient/', PatientRegistration.as_view(), name='register-patient'),
    path('login/', LoginView.as_view(), name='login'),
    path('video-stream/', video_stream, name='video_stream'),
    path('start-video-processing/', start_video_processing, name='start_video_processing'),
    path('capture-photo/', CapturePhotoView.as_view(), name='capture_photo'),  # capture the photo
    path('delete-user/<int:user_id>/', delete_user, name='delete_user'),


    # paths for testing in the postman, later there will be one path ----------------
    path('addRecording/', AddRecordingView.as_view(), name='add_recording'),
    path('addFrame/', AddFrameView.as_view(), name='add_frame'),
    path('addLandmarks/', AddFrameLandmarksView.as_view(), name='add_landmarks'),
    # -------------------------------------



    path('', TemplateView.as_view(template_name='index.html')),

]