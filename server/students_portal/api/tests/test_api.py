from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from api.models import User, Subject, Assignment, StudentAssignment
from django.utils import timezone

class APITestCase(APITestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create(
            name="Test User",
            email="test@example.com",
            password="testpass123",
            role="student"
        )
        
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

    def test_user_list(self):
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

    def test_user_detail(self):
        url = reverse('user-detail', args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'test@example.com')

    def test_subject_list(self):
        url = reverse('subject-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

    def test_subject_detail(self):
        url = reverse('subject-detail', args=[self.subject.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Mathematics')

    def test_assignment_list(self):
        url = reverse('assignment-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

    def test_assignment_detail(self):
        url = reverse('assignment-detail', args=[self.assignment.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Math Test')

    def test_create_student_assignment(self):
        url = reverse('studentassignment-list')
        data = {
            'student': self.user.id,
            'assignment': self.assignment.id,
            'answers': {'q1': '4'},
            'status': 'completed',
            'score': 100
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(StudentAssignment.objects.count(), 1)
        self.assertEqual(StudentAssignment.objects.get().score, 100)

    def test_get_csrf_token(self):
        url = reverse('get-csrf-token')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('csrfToken' in response.data)

    def test_register_new_user(self):
        url = reverse('register')
        data = {
            'name': 'New User',
            'email': 'new@example.com',
            'password': 'newpass123',
            'role': 'student'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')
        self.assertTrue(User.objects.filter(email='new@example.com').exists())

    def test_user_login(self):
        url = reverse('login')
        data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')
        self.assertTrue('token' in response.data)

    def test_generate_custom_assignment(self):
        url = reverse('generate-custom-assignment')
        data = {
            'topic': 'Algebra',
            'subject': 'Mathematics',
            'student_email': 'test@example.com'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')
