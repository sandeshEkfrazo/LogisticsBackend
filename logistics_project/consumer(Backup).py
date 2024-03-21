# chat/consumers.py


import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from time import sleep
import asyncio
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from django.db.models.signals import post_save
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.observer import model_observer
from djangochannelsrestframework import permissions

from masters.serializers import *
from masters.models import *

class UpdateModelChange(GenericAsyncAPIConsumer):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permissions = (permissions.AllowAny,)

    async def connect(self, **kwargs):        
        await self.model_change.subscribe()
        # await super().connect()
        await self.accept()

    @model_observer(Status)
    async def model_change(self, message, observer=None, **kwargs):
        await self.send_json(message)

    @model_change.serializer
    def model_serialize(self, instance, action, **kwargs):
        return dict(data=StatusSerializer(instance=instance).data, action=action.value)



# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         # Importing models after the app registry is ready
#         from masters.models import Status

#         await self.accept()  

#         status_obj = await sync_to_async(Status.objects.last)()
#         serialized_data = json.dumps(status_obj_to_dict(status_obj)) if status_obj else '{}'

#         await self.send(text_data=serialized_data)
#         await asyncio.sleep(1)     
        

#     async def disconnect(self, close_code):
#         pass

#     async def receive(self, text_data):
#         from masters.models import Status
#         #if text_data:
#         status_obj = await sync_to_async(Status.objects.last)()
#         serialized_data = json.dumps(status_obj_to_dict(status_obj)) if status_obj else '{}'

#         await self.send(text_data=serialized_data)
#         await asyncio.sleep(1)
            
# def status_obj_to_dict(status_obj):
#     return {
#         'id': status_obj.id,
#         # Add more fields here
#     }

