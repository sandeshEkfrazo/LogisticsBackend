from django.urls import re_path, path

from . import consumer

# websocket_urlpatterns = [
#     re_path(r'ws/get/$', consumer.MySyncConsumer.as_asgi()),
#     # re_path(r'ws/change/$', consumer.UpdateModelChange.as_asgi()),
#     # re_path(r'ws/change/$', consumer.UpdateModelChange.as_asgi()),
#     # path('ws/change/', consumer.UpdateModelChange.as_asgi())
# ]


websocket_urlpatterns = [
    # path('ws/get/', consumer.MySyncConsumer.as_asgi()),
    path('ws/get/', consumer.MyAsyncConsumer.as_asgi()),
    # path('ws/get-data/', consumer.StatusConsumer.as_asgi())
]


