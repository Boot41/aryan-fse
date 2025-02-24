# /home/aryan/Documents/project/server/students_portal/api/webrtc/views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from livekit import api
from livekit.api import ListRoomsRequest,LiveKitAPI, CreateRoomRequest, RoomConfiguration
import json
import os
from django.core.exceptions import ValidationError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models import StudentAssignment
from django.utils import timezone
from datetime import timedelta

api_key = os.getenv('LIVEKIT_API_KEY')
api_secret = os.getenv('LIVEKIT_API_SECRET')
livkit_server_url = os.getenv('LIVEKIT_SERVER_URL')
# Constants for error messages

@csrf_exempt
async def room_assignment(request):
    if request.method == 'OPTIONS':
        response = JsonResponse({})
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type'
        return response

    lkapi = LiveKitAPI(url=settings.LIVEKIT_SERVER_URL)
    try:
        rooms = await lkapi.room.list_rooms(ListRoomsRequest())
        print(rooms)
        return JsonResponse({"rooms": [room.name for room in rooms.rooms]})
    except Exception as e:
        print(f"Error listing rooms: {e}")
        return JsonResponse({"error": "Failed to list rooms"}, status=500)
    finally:
        await lkapi.aclose()

@csrf_exempt
async def create_room(request):
    if request.method == 'OPTIONS':
        response = JsonResponse({})
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type'
        return response

    lkapi = LiveKitAPI(url=settings.LIVEKIT_SERVER_URL)
    try:
        user_name = request.data.get('name')
        room_name = request.data.get('room')

        if not user_name or not room_name:
            return Response({'error': 'Missing name or room name'}, status=400)

        assignment_details = get_latest_assignment_details(room_name)
        metadata = "No recent assignments"
        
        if assignment_details:
            metadata = f"Subject: {assignment_details['subject']}, Topic: {assignment_details['topic']}"
            if assignment_details['score'] is not None:
                metadata += f", Score: {assignment_details['score']:.2f}%"
        print(metadata)
        room = await lkapi.room.create_room(
            CreateRoomRequest(
                name="myroom",
                metadata=metadata,
                empty_timeout=10 * 60,
                max_participants=2,
            )
        )
        return JsonResponse({"room": room.name})
    except Exception as e:
        print(f"Error creating room: {e}")
        return JsonResponse({"error": "Failed to create room"}, status=500)
    finally:
        await lkapi.aclose()


def validate_request_data(data):
    """Validate incoming request data"""
    print(data)
    if not isinstance(data, dict):
        raise ValidationError(ERROR_MESSAGES['invalid_json'])
        
    room_name = data.get('room', 'default-room')
    user_name = data.get('name', 'anonymous')
    
    if not room_name or not isinstance(room_name, str):
        raise ValidationError(ERROR_MESSAGES['invalid_room_name'])
        
    if not user_name or not isinstance(user_name, str):
        raise ValidationError(ERROR_MESSAGES['invalid_user_name'])
        
    return room_name, user_name

ERROR_MESSAGES = {
    'invalid_method': 'Only GET requests are allowed',
    'invalid_json': 'Invalid JSON format in request body',
    'missing_credentials': 'LiveKit credentials are not configured',
    'invalid_room_name': 'Room name must be a non-empty string',
    'invalid_user_name': 'User name must be a non-empty string',
    'token_generation_failed': 'Failed to generate access token'
}

def get_latest_assignment_details(email):
    try:
        thirty_days_ago = timezone.now() - timedelta(days=30)
        latest_assignment = StudentAssignment.objects.filter(
            student__email=email,
            assigned_at__gte=thirty_days_ago
        ).order_by('-assigned_at').first()

        if latest_assignment:
            return {
                'subject': latest_assignment.assignment.subject.name,
                'topic': latest_assignment.assignment.topic,
                'score': float(latest_assignment.score) if latest_assignment.score else None
            }
        return None
    except Exception as e:
        print(f"Error getting latest assignment: {e}")
        return None

@api_view(['POST'])
def generate_token(request):
    try:
        user_name = request.data.get('name')
        room_name = request.data.get('room')

        if not user_name or not room_name:
            return Response({'error': 'Missing name or room name'}, status=400)

        assignment_details = get_latest_assignment_details(room_name)
        metadata = "meta data received from client "
        
        print(metadata)
        token = api.AccessToken(api_key, api_secret) \
            .with_identity(user_name) \
            .with_name(user_name) \
            .with_metadata(metadata)\
            .with_grants(api.VideoGrants(
                room_join=True,
                room=room_name,
            ))

        return Response({
            'participantToken': token.to_jwt(),
            'serverUrl': livkit_server_url,
            'assignmentDetails': assignment_details
        })
    except Exception as e:
        print(str(e))
        return Response({'error': str(e)}, status=500)
