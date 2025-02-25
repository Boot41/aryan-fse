from django.test import TestCase, Client
from django.urls import reverse
from api.models import User, Subject, Assignment, StudentAssignment
import json

class APIEndpointTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Create test user
        self.user_data = {
            "name": "Test User",
            "email": "test@example.com",
            "password": "testpass123",
            "role": "student"
        }
        self.user = User.objects.create(**self.user_data)
        
        # Create test subject
        self.subject = Subject.objects.create(
            name="Mathematics",
            description="Mathematics subject"
        )
        
        # Create test assignment
        self.assignment = Assignment.objects.create(
            title="Math Test",
            description="Test description",
            subject=self.subject,
            topic="Algebra",
            questions={"q1": "What is 2+2?"},
            assignment_type="general"
        )

    def test_register_endpoint(self):
        """Test user registration endpoint"""
        new_user_data = {
            "name": "New User",
            "email": "new@example.com",
            "password": "newpass123",
            "role": "student"
        }
        response = self.client.post(
            '/api/register/',
            data=json.dumps(new_user_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

    def test_login_endpoint(self):
        """Test user login endpoint"""
        login_data = {
            "email": "test@example.com",
            "password": "testpass123"
        }
        response = self.client.post(
            '/api/login/',
            data=json.dumps(login_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

    def test_get_user_assignments_endpoint(self):
        """Test getting user assignments endpoint"""
        StudentAssignment.objects.create(
            student=self.user,
            assignment=self.assignment,
            submission={},
            status="pending"
        )
        response = self.client.get(
            '/api/assignments/',
            {'email': 'test@example.com'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue('assignments' in response.json())

    def test_take_assignment_endpoint(self):
        """Test taking an assignment endpoint"""
        data = {
            "student_email": "test@example.com",
            "assignment_id": self.assignment.id,
            "score": 85  # Add score as required by the API
        }
        response = self.client.post(
            '/api/take-assignment/',
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

    def test_get_subjects_and_topics_endpoint(self):
        """Test getting subjects and topics endpoint"""
        # Create a student assignment to ensure there's a topic
        StudentAssignment.objects.create(
            student=self.user,
            assignment=self.assignment,
            submission={},
            status="pending"
        )
        
        response = self.client.get('/api/subjects-and-topics/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(isinstance(data, dict))
