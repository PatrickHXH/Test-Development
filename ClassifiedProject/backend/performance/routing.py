from django.urls import re_path

from performance import consumers

websocket_urlpatterns = [
    #(?P<room_name>\w+) 正则表达式
    re_path(r'ws/performance/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/performance/cpu/$', consumers.CPUConsumer.as_asgi()),
    re_path(r'ws/performance/memory/$', consumers.MemoryConsumer.as_asgi()),
]