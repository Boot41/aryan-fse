# /home/aryan/Documents/project/server/students_portal/api/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, SubjectViewSet, EnrollmentViewSet, AssessmentViewSet, ChatbotInteractionViewSet, SubjectTeacherViewSet, TeacherStudentMappingViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'subjects', SubjectViewSet)
router.register(r'enrollments', EnrollmentViewSet)
router.register(r'assessments', AssessmentViewSet)
router.register(r'chatbot-interactions', ChatbotInteractionViewSet)
router.register(r'subject-teachers', SubjectTeacherViewSet)
router.register(r'teacher-student-mappings', TeacherStudentMappingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]