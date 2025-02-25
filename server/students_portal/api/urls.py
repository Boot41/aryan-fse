# /home/aryan/Documents/project/server/students_portal/api/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, SubjectViewSet, AssignmentViewSet, StudentAssignmentViewSet,
    get_csrf_token, login_view, register_view, get_user_assignments, get_user_profile, take_assignment,
    generate_custom_assignment, get_subjects_and_topics
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'subjects', SubjectViewSet)
router.register(r'assignments', AssignmentViewSet)
router.register(r'student-assignments', StudentAssignmentViewSet)

from api.livekit.views import generate_token, room_assignment, create_room
urlpatterns = [
    path('assignments/', get_user_assignments, name='get_user_assignments'),  # Custom endpoint
    path('take-assignment/', take_assignment, name='take_assignment'),  # New endpoint for taking assignments
    path('profile/', get_user_profile, name='get_user_profile'),  # Custom endpoint
    path('generate-custom-assignment/', generate_custom_assignment, name='generate-custom-assignment'),  # New endpoint for generating assignments
    path('subjects-and-topics/', get_subjects_and_topics, name='subjects-and-topics'),  # New endpoint for getting subjects and topics
    path('', include(router.urls)),  # Default router URLs
    path('csrf-token/', get_csrf_token, name='csrf-token'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('chat-room-token/', generate_token, name='generate_token'),
    path('room-assignment/', room_assignment, name='room-assignment'),
    path('api/create-room/', create_room, name='create-room'),
]