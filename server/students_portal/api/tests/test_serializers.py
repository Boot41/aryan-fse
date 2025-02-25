from django.test import TestCase
from api.models import User, Subject, Assignment, StudentAssignment
from api.serializers import UserSerializer, SubjectSerializer, AssignmentSerializer, StudentAssignmentSerializer
from django.utils import timezone

class SerializerTestCase(TestCase):
    def setUp(self):
        self.user_data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'password': 'testpass123',
            'role': 'student'
        }
        self.user = User.objects.create(**self.user_data)
        
        self.subject_data = {
            'name': 'Mathematics',
            'description': 'Mathematics subject'
        }
        self.subject = Subject.objects.create(**self.subject_data)
        
        self.assignment_data = {
            'title': 'Math Test',
            'description': 'Test description',
            'subject': self.subject,
            'topic': 'Algebra',
            'questions': {'q1': 'What is 2+2?'}
        }
        self.assignment = Assignment.objects.create(**self.assignment_data)
        
        self.student_assignment_data = {
            'student': self.user,
            'assignment': self.assignment,
            'answers': {'q1': '4'},
            'status': 'completed',
            'score': 100
        }
        self.student_assignment = StudentAssignment.objects.create(**self.student_assignment_data)

    def test_user_serializer(self):
        serializer = UserSerializer(instance=self.user)
        data = serializer.data
        self.assertEqual(data['name'], 'Test User')
        self.assertEqual(data['email'], 'test@example.com')
        self.assertEqual(data['role'], 'student')

    def test_subject_serializer(self):
        serializer = SubjectSerializer(instance=self.subject)
        data = serializer.data
        self.assertEqual(data['name'], 'Mathematics')
        self.assertEqual(data['description'], 'Mathematics subject')

    def test_assignment_serializer(self):
        serializer = AssignmentSerializer(instance=self.assignment)
        data = serializer.data
        self.assertEqual(data['title'], 'Math Test')
        self.assertEqual(data['description'], 'Test description')
        self.assertEqual(data['topic'], 'Algebra')
        self.assertEqual(data['questions'], {'q1': 'What is 2+2?'})

    def test_student_assignment_serializer(self):
        serializer = StudentAssignmentSerializer(instance=self.student_assignment)
        data = serializer.data
        self.assertEqual(data['answers'], {'q1': '4'})
        self.assertEqual(data['status'], 'completed')
        self.assertEqual(data['score'], 100)

    def test_user_serializer_validation(self):
        invalid_data = {
            'name': '',
            'email': 'invalid-email',
            'password': '',
            'role': 'invalid-role'
        }
        serializer = UserSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertTrue('name' in serializer.errors)
        self.assertTrue('email' in serializer.errors)
        self.assertTrue('password' in serializer.errors)

    def test_subject_serializer_validation(self):
        invalid_data = {
            'name': '',
            'description': ''
        }
        serializer = SubjectSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertTrue('name' in serializer.errors)

    def test_assignment_serializer_validation(self):
        invalid_data = {
            'title': '',
            'description': '',
            'subject': None,
            'topic': '',
            'questions': None
        }
        serializer = AssignmentSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertTrue('title' in serializer.errors)
        self.assertTrue('subject' in serializer.errors)
