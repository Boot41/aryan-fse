# /home/aryan/Documents/project/server/students_portal/api/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, SubjectViewSet, EnrollmentViewSet, AssessmentViewSet,
    ChatbotInteractionViewSet, SubjectTeacherViewSet, TeacherStudentMappingViewSet,
    get_csrf_token, login_view
)
from .webrtc import views as webrtc_views

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'subjects', SubjectViewSet)
router.register(r'enrollments', EnrollmentViewSet)
router.register(r'assessments', AssessmentViewSet)
router.register(r'chatbot-interactions', ChatbotInteractionViewSet)
router.register(r'subject-teachers', SubjectTeacherViewSet)
router.register(r'teacher-student-mappings', TeacherStudentMappingViewSet)
from api.webrtc.views import generate_token, room_assignment, create_room
urlpatterns = [
    path('', include(router.urls)),
    path('csrf-token/', get_csrf_token, name='csrf-token'),
    path('login/', login_view, name='login'),
    # path('signup/', signup_view, name='signup'),
    path('chat-room-token/', generate_token, name='generate_token'),
    path('room-assignment/', room_assignment, name='room-assignment'),
    path('api/create-room/', create_room, name='create-room'),
    # path('process-audio/', webrtc_views.process_audio, name='process_audio'),
]