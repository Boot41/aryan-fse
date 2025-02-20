# /home/aryan/Documents/project/server/students_portal/api/tests.py

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User, Subject, TeacherStudentMapping

class AssessmentTests(APITestCase):
    def setUp(self):
        self.teacher = User.objects.create_user(
            email='teacher@example.com',
            name='Teacher',
            role='teacher',
            password='teacherpassword123'
        )
        self.student = User.objects.create_user(
            email='student@example.com',
            name='Student',
            role='student',
            password='studentpassword123'
        )
        self.subject = Subject.objects.create(
            name='Physics',
            description='Introduction to physics'
        )
        self.assessment_data = {
            'student': self.student.id,
            'subject': self.subject.id,
            'teacher': self.teacher.id,
            'assessment_data': {'questions': []},
            'result': 85.5
        }
        self.assessment = Assessment.objects.create(**self.assessment_data)
        self.url = reverse('assessment-list')

    def test_create_assessment(self):
        response = self.client.post(self.url, self.assessment_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Assessment.objects.count(), 2)

    def test_get_assessment(self):
        url = reverse('assessment-detail', args=[self.assessment.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['student'], self.assessment_data['student'])

class UserTests(APITestCase):
    def setUp(self):
        self.user_data = {
            'email': 'test@example.com',
            'name': 'Test User',
            'role': 'student',
            'password': 'testpassword123'
        }
        self.user = User.objects.create_user(**self.user_data)
        self.url = reverse('user-list')

    def test_create_user(self):
        response = self.client.post(self.url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

    def test_get_user(self):
        url = reverse('user-detail', args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user_data['email'])

class SubjectTests(APITestCase):
    def setUp(self):
        self.subject_data = {
            'name': 'Mathematics',
            'description': 'Introduction to advanced mathematics',
        }
        self.subject = Subject.objects.create(**self.subject_data)
        self.url = reverse('subject-list')

    def test_create_subject(self):
        response = self.client.post(self.url, self.subject_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Subject.objects.count(), 2)

    def test_get_subject(self):
        url = reverse('subject-detail', args=[self.subject.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.subject_data['name'])

class TeacherStudentMappingTests(APITestCase):
    def setUp(self):
        self.teacher = User.objects.create_user(
            email='teacher@example.com',
            name='Teacher',
            role='teacher',
            password='teacherpassword123'
        )
        self.student = User.objects.create_user(
            email='student@example.com',
            name='Student',
            role='student',
            password='studentpassword123'
        )
        self.subject = Subject.objects.create(
            name='Physics',
            description='Introduction to physics'
        )
        self.mapping_data = {
            'teacher': self.teacher.id,
            'student': self.student.id,
            'subject': self.subject.id
        }
        self.mapping = TeacherStudentMapping.objects.create(**self.mapping_data)
        self.url = reverse('teacherstudentmapping-list')

    def test_create_mapping(self):
        response = self.client.post(self.url, self.mapping_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TeacherStudentMapping.objects.count(), 2)

    def test_get_mapping(self):
        url = reverse('teacherstudentmapping-detail', args=[self.mapping.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['teacher'], self.mapping_data['teacher'])