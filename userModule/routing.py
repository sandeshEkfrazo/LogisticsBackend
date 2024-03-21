from django.urls import path, re_path
from .consumers import *

websocket_urlpatterns = [
    path('ws/psc/', PostConsumer.as_asgi())
]
