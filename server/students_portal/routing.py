# /home/aryan/Documents/project/server/students_portal/routing.py

from django.urls import re_path
from channels.routing import ProtocolTypeRouter, URLRouter
from .api.webrtc.signaling import WebRTCSignaling

websocket_urlpatterns = [
    re_path(r'ws/webrtc/$', WebRTCSignaling.as_asgi()),
]

application = ProtocolTypeRouter({
    'websocket': URLRouter(websocket_urlpatterns),
})