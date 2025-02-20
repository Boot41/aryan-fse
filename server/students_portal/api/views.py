# /home/aryan/Documents/project/server/students_portal/api/views.py

from rest_framework import viewsets
from .models import User, Subject, Enrollment, Assessment, ChatbotInteraction, SubjectTeacher, TeacherStudentMapping
from .serializers import UserSerializer, SubjectSerializer, EnrollmentSerializer, AssessmentSerializer, ChatbotInteractionSerializer, SubjectTeacherSerializer, TeacherStudentMappingSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer

class AssessmentViewSet(viewsets.ModelViewSet):
    queryset = Assessment.objects.all()
    serializer_class = AssessmentSerializer

class ChatbotInteractionViewSet(viewsets.ModelViewSet):
    queryset = ChatbotInteraction.objects.all()
    serializer_class = ChatbotInteractionSerializer

class SubjectTeacherViewSet(viewsets.ModelViewSet):
    queryset = SubjectTeacher.objects.all()
    serializer_class = SubjectTeacherSerializer

class TeacherStudentMappingViewSet(viewsets.ModelViewSet):
    queryset = TeacherStudentMapping.objects.all()
    serializer_class = TeacherStudentMappingSerializer

# Create your views here.
