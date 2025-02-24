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
from .models import User, Subject, Assignment, StudentAssignment
from .serializers import UserSerializer, SubjectSerializer, AssignmentSerializer, StudentAssignmentSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer

class StudentAssignmentViewSet(viewsets.ModelViewSet):
    queryset = StudentAssignment.objects.all()
    serializer_class = StudentAssignmentSerializer

@api_view(['GET'])
@permission_classes([AllowAny])
def get_csrf_token(request):
    return JsonResponse({'csrfToken': get_token(request)})

@csrf_exempt
def register_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            email = data.get('email')
            password = data.get('password')
            role = data.get('role', 'student')

            if not all([name, email, password]):
                return JsonResponse({'status': 'error', 'message': 'All fields are required'}, status=400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({'status': 'error', 'message': 'Email already exists'}, status=400)

            user = User.objects.create(
                name=name,
                email=email,
                password=password,  # Note: We should hash this in production
                role=role
            )

            return JsonResponse({
                'status': 'success',
                'user': {
                    'id': user.id,
                    'name': user.name,
                    'email': user.email,
                    'role': user.role
                }
            })
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')

            if not all([email, password]):
                return JsonResponse({'status': 'error', 'message': 'Email and password are required'}, status=400)

            try:
                user = User.objects.get(email=email)
                if user.password == password:  # Note: In production, use proper password hashing
                    return JsonResponse({
                        'status': 'success',
                        'user': {
                            'id': user.id,
                            'name': user.name,
                            'email': user.email,
                            'role': user.role
                        },
                        'token': 'dummy-token'  # In production, generate a proper JWT token
                    })
                else:
                    return JsonResponse({'status': 'error', 'message': 'Invalid credentials'}, status=401)
            except User.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Invalid credentials'}, status=401)

        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

# @csrf_exempt
# def get_user_assignments(request):
#     return JsonResponse({'status': 'success', 'assignments': []})

@csrf_exempt
def get_user_assignments(request):
    if request.method == 'GET':
        try:
            email = request.GET.get('email')
            if not email:
                return JsonResponse({'status': 'error', 'message': 'Email parameter is required'}, status=400)

            user = User.objects.filter(email=email).first()
            if not user:
                return JsonResponse({'status': 'error', 'message': 'User not found'}, status=404)

            student_assignments = StudentAssignment.objects.filter(student=user)
            assignments_data = []

            for sa in student_assignments:
                assignment_data = {
                    'id': sa.assignment.id,
                    'title': sa.assignment.title,
                    'description': sa.assignment.description,
                    'status': sa.status,
                    'test_data': {
                        'duration': sa.assignment.duration,
                        'totalQuestions': sa.assignment.total_questions
                    },
                    'result': sa.score,
                }
                assignments_data.append(assignment_data)
            
            return JsonResponse({'status': 'success', 'assignments': assignments_data})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)

@csrf_exempt
def get_user_profile(request):
    if request.method == 'GET':
        try:
            email = request.GET.get('email')
            if not email:
                return JsonResponse({'status': 'error', 'message': 'Email parameter is required'}, status=400)

            user = User.objects.filter(email=email).first()
            if not user:
                return JsonResponse({'status': 'error', 'message': 'User not found'}, status=404)

            # Get student's assignments and calculate stats
            student_assignments = StudentAssignment.objects.filter(student=user)
            total_assignments = student_assignments.count()
            completed_assignments = student_assignments.filter(status='completed').count()
            total_score = sum(sa.score or 0 for sa in student_assignments.filter(status='completed'))
            average_score = total_score / completed_assignments if completed_assignments > 0 else 0

            profile_data = {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'role': user.role,
                'created_at': user.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at': user.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
                'stats': {
                    'total_assignments': total_assignments,
                    'completed_assignments': completed_assignments,
                    'pending_assignments': total_assignments - completed_assignments,
                    'total_score': float(total_score),
                    'average_score': float(average_score)
                }
            }

            return JsonResponse({'status': 'success', 'profile': profile_data})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)