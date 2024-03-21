

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter

import userModule.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'logistics_project.settings')

application = ProtocolTypeRouter({
    'http':  get_asgi_application(),
    'websocket': URLRouter(
        userModule.routing.websocket_urlpatterns
    )
})

