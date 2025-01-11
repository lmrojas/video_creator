from django.urls import re_path
from video_app.consumers import VideoProcessingConsumer

websocket_urlpatterns = [
    re_path(r'ws/video/(?P<project_id>\w+)/$', VideoProcessingConsumer.as_asgi()),
] 