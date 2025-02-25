from django.test import TestCase, Client
from django.urls import reverse
from api.models import User
import json

class LiveKitIntegrationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            name="Test User",
            email="test@example.com",
            password="testpass123",
            role="student"
        )

    def test_generate_token_endpoint(self):
        """Test generating LiveKit token endpoint"""
        data = {
            "room": "test_room",
            "name": "test_user_name",
            "topic": "Algebra",
            "subject": "Mathematics"
        }
        response = self.client.post(
            '/api/chat-room-token/',
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

    def test_room_assignment_endpoint(self):
        """Test room assignment endpoint"""
        data = {
            "room_name": "test_room",
            "topic": "Algebra",
            "subject": "Mathematics"
        }
        response = self.client.post(
            '/api/room-assignment/',
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
