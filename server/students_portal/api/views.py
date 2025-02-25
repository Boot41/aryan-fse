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
from django.utils import timezone

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

@csrf_exempt
def take_assignment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            student_email = data.get('student_email')
            assignment_id = data.get('assignment_id')
            score = data.get('score')

            if not all([student_email, assignment_id, score]):
                return JsonResponse({
                    'status': 'error',
                    'message': 'student_email, assignment_id and score are required'
                }, status=400)

            # Get the student and assignment
            student = User.objects.filter(email=student_email).first()
            assignment = Assignment.objects.filter(id=assignment_id).first()

            if not student or not assignment:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Student or Assignment not found'
                }, status=404)

            # Create or update the student assignment
            student_assignment, created = StudentAssignment.objects.get_or_create(
                student=student,
                assignment=assignment,
                defaults={
                    'status': 'completed',
                    'score': score,
                    'submitted_at': timezone.now(),
                    'graded_at': timezone.now()
                }
            )

            if not created:
                student_assignment.status = 'completed'
                student_assignment.score = score
                student_assignment.submitted_at = timezone.now()
                student_assignment.graded_at = timezone.now()
                student_assignment.save()

            return JsonResponse({
                'status': 'success',
                'message': 'Assignment score saved successfully',
                'data': {
                    'student_assignment_id': student_assignment.id,
                    'score': student_assignment.score
                }
            })

        except json.JSONDecodeError:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid JSON data'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)

    return JsonResponse({
        'status': 'error',
        'message': 'Method not allowed'
    }, status=405)

@csrf_exempt
def generate_custom_assignment(request):
    if request.method != 'POST':
        return JsonResponse({
            'status': 'error',
            'message': 'Only POST method is allowed'
        }, status=405)

    try:
        data = json.loads(request.body)
        topic = data.get('topic')
        subject = data.get('subject')
        student_email = data.get('student_email')
        print(topic, subject, student_email,data)
        if not all([topic, subject, student_email]):
            return JsonResponse({
                'status': 'error',
                'message': 'topic, subject, and student_email are required'
            }, status=400)

        # Get the student
        student = User.objects.filter(email=student_email).first()
        if not student:
            return JsonResponse({
                'status': 'error',
                'message': 'Student not found'
            }, status=404)

        try:
            from .utils.llm_utils import generate_assignment_questions
            assignment_data = generate_assignment_questions(topic, subject)

            # Create a new assignment
            subject_obj, _ = Subject.objects.get_or_create(
                name=subject,
                defaults={'description': f'Subject for {subject} assignments'}
            )

            assignment = Assignment.objects.create(
                title=assignment_data['title'],
                description=f'Custom generated assignment for {topic} in {subject}',
                questions=json.dumps(assignment_data['questions']),
                subject=subject_obj,
                duration=30,  # Default 30 minutes
                total_questions=len(assignment_data['questions'])
            )

            # Create a student assignment
            StudentAssignment.objects.create(
                student=student,
                assignment=assignment,
                status='pending'
            )

            return JsonResponse({
                'status': 'success',
                'message': 'Custom assignment generated successfully',
                'data': {
                    'assignment_id': assignment.id,
                    'title': assignment.title,
                    'description': assignment.description
                }
            })

        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'Error generating assignment: {str(e)}'
            }, status=500)

    except json.JSONDecodeError:
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

@csrf_exempt
def get_subjects_and_topics(request):
    if request.method != 'GET':
        return JsonResponse({
            'status': 'error',
            'message': 'Only GET method is allowed'
        }, status=405)

    try:
        # Get all subjects
        subjects = Subject.objects.all()
        
        # Create a dictionary to store subjects and their topics
        subjects_data = {}
        
        for subject in subjects:
            # Get assignments for this subject
            assignments = Assignment.objects.filter(subject=subject)
            
            # Extract topics from assignments
            topics = set()  # Using set to avoid duplicates
            for assignment in assignments:
                # Add title words as potential topics (excluding common words)
                words = assignment.title.lower().split()
                topics.update([word for word in words if len(word) > 3])  # Only words longer than 3 chars
                
                # Add description words as potential topics
                if assignment.description:
                    desc_words = assignment.description.lower().split()
                    topics.update([word for word in desc_words if len(word) > 3])
            
            # Add some default topics if none found
            if not topics and subject.name.lower() == 'advanced mathematics':
                topics = {'calculus', 'algebra', 'statistics', 'trigonometry', 'probability'}
            elif not topics and subject.name.lower() == 'physics':
                topics = {'mechanics', 'thermodynamics', 'electromagnetism', 'optics', 'quantum'}
            elif not topics and 'computer' in subject.name.lower():
                topics = {'algorithms', 'programming', 'databases', 'networking', 'security'}
            
            # Convert set to sorted list for JSON serialization
            subjects_data[subject.name] = {
                'description': subject.description,
                'topics': sorted(list(topics))
            }
        
        return JsonResponse({
            'status': 'success',
            'data': subjects_data
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)