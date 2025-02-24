# /home/aryan/Documents/project/server/students_portal/api/serializers.py

from rest_framework import serializers
from .models import User, Subject, Assignment, StudentAssignment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = '__all__'

class StudentAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAssignment
        fields = '__all__'