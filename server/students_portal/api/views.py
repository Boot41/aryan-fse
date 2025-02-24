# /home/aryan/Documents/project/server/students_portal/api/views.py

from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from django.middleware.csrf import get_token
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import RefreshToken
import json
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

@api_view(['GET'])
@permission_classes([AllowAny])
def get_csrf_token(request):
    return JsonResponse({'csrfToken': get_token(request)})

@csrf_exempt  # Disable CSRF for API (not recommended for production)
def login_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)  # Django's session login
            return JsonResponse({"message": "Login successful"})
        return JsonResponse({"error": "Invalid credentials"}, status=400)

    return JsonResponse({"error": "POST request required"}, status=405)

# @csrf_exempt
# def signup_view(request):
#     if request.method == "POST":
#         try:
#             data = json.loads(request.body)
#             username = data.get('username')
#             email = data.get('email')
#             password = data.get('password')
#             role = data.get('role', 'student')  # Default role is student if not specified

#             # Validate required fields
#             if not all([username, email, password]):
#                 return JsonResponse({
#                     'error': 'Please provide username, email and password'
#                 }, status=400)

#             # Check if user already exists
#             if User.objects.filter(username=username).exists():
#                 return JsonResponse({
#                     'error': 'Username already exists'
#                 }, status=400)
            
#             if User.objects.filter(email=email).exists():
#                 return JsonResponse({
#                     'error': 'Email already exists'
#                 }, status=400)

#             # Create new user
#             user = User.objects.create_user(
#                 username=username,
#                 email=email,
#                 password=password,
#                 role=role
#             )

#             # Log the user in
#             login(request, user)

#             return JsonResponse({
#                 'message': 'User created successfully',
#                 'user': {
#                     'username': user.username,
#                     'email': user.email,
#                     'role': user.role
#                 }
#             })

#         except json.JSONDecodeError:
#             return JsonResponse({'error': 'Invalid JSON'}, status=400)
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)

#     return JsonResponse({"error": "POST request required"}, status=405)