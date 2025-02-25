from django.test import TestCase, Client
from django.urls import reverse
from api.models import User, Subject, Assignment, StudentAssignment
from django.utils import timezone
import json

class ViewsTestCase(TestCase):
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
            questions={"q1": "What is 2+2?"}
        )

    def test_register_view(self):
        new_user_data = {
            "name": "New User",
            "email": "new@example.com",
            "password": "newpass123",
            "role": "student"
        }
        response = self.client.post(
            reverse('register'),
            data=json.dumps(new_user_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')
        self.assertEqual(response.json()['user']['email'], 'new@example.com')

    def test_register_view_duplicate_email(self):
        response = self.client.post(
            reverse('register'),
            data=json.dumps(self.user_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['status'], 'error')
        self.assertEqual(response.json()['message'], 'Email already exists')

    def test_login_view_success(self):
        login_data = {
            "email": "test@example.com",
            "password": "testpass123"
        }
        response = self.client.post(
            reverse('login'),
            data=json.dumps(login_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')
        self.assertEqual(response.json()['user']['email'], 'test@example.com')

    def test_login_view_invalid_credentials(self):
        login_data = {
            "email": "test@example.com",
            "password": "wrongpass"
        }
        response = self.client.post(
            reverse('login'),
            data=json.dumps(login_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_get_user_assignments(self):
        StudentAssignment.objects.create(
            student=self.user,
            assignment=self.assignment,
            answers={},
            status="pending"
        )
        response = self.client.get(
            reverse('user-assignments'),
            {'email': 'test@example.com'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')
        self.assertTrue(len(response.json()['assignments']) > 0)

    def test_get_user_profile(self):
        response = self.client.get(
            reverse('user-profile'),
            {'email': 'test@example.com'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')
        self.assertEqual(response.json()['user']['email'], 'test@example.com')

    def test_take_assignment(self):
        assignment_data = {
            "student_email": "test@example.com",
            "assignment_id": self.assignment.id,
            "answers": {"q1": "4"}
        }
        response = self.client.post(
            reverse('take-assignment'),
            data=json.dumps(assignment_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')

    def test_generate_custom_assignment(self):
        data = {
            "topic": "Algebra",
            "subject": "Mathematics",
            "student_email": "test@example.com"
        }
        response = self.client.post(
            reverse('generate-custom-assignment'),
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')

    def test_get_subjects_and_topics(self):
        response = self.client.get(reverse('subjects-and-topics'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Mathematics' in response.json())
