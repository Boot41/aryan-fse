# /home/aryan/Documents/project/server/students_portal/api/serializers.py

from rest_framework import serializers
from .models import User, Subject, Enrollment, Assessment, ChatbotInteraction, SubjectTeacher, TeacherStudentMapping

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = '__all__'

class AssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assessment
        fields = '__all__'

class ChatbotInteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatbotInteraction
        fields = '__all__'

class SubjectTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectTeacher
        fields = '__all__'

class TeacherStudentMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherStudentMapping
        fields = '__all__'