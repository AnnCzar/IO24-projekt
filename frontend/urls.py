from django.urls import path
from django.views.generic import TemplateView

from FaceMotionMonitorApp.views import GetUserRoleView
from frontend.views import index

urlpatterns = [
    path('', index),
    path('', TemplateView.as_view(template_name='index.html')),
]