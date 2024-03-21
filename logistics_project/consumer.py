# chat/consumers.py


from channels.consumer import SyncConsumer, AsyncConsumer
from asgiref.sync import async_to_sync
from channels.exceptions import StopConsumer

from masters.models import *
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
# from masters.serializers import *

# from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
# from djangochannelsrestframework.mixins import ListModelMixin
# from djangochannelsrestframework.observer import model_observer
# from djangochannelsrestframework import permissions


# class StatusConsumer(GenericAsyncAPIConsumer):
#     queryset = Status.objects.all()

#     async def connect(self, **kwargs):
#         await self.model_change.subscribe()
#         await super().connect()

#     @model_observer(Status)
#     async def model_change(self, message, observer=None, **kwargs):
#         await self.send_json(message['data'])

#     @model_change.serializer
#     def model_serialize(self, instance, action, **kwargs):
#         return dict(data=StatusSerializer(instance=instance).data, action=action.value)
    




class MySyncConsumer(SyncConsumer):
    def websocket_connect(self, event):
        print("connected", event, self.channel_layer, self.channel_name)

        async_to_sync(self.channel_layer.group_add)(
            'driver', self.channel_name
        )

        self.send({
            'type': 'websocket.accept'
        })

    def websocket_receive(self, event):
        print("recived ", event)

        async_to_sync(self.channel_layer.group_send)('driver', {
            'type': 'chat.message',
            'message': event['text']
        })


    def chat_message(self, event):
        # print('chat', event)
        self.send({
            'type': 'websocket.send',
            'text': event['message']
        })


    def websocket_disconnect(self, event):
        print("dic connected", event, self.channel_layer, self.channel_name)

        async_to_sync(self.channel_layer.group_discard)('driver', self.channel_name)
        raise StopConsumer()
    

class MyAsyncConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("connected", event, self.channel_layer, self.channel_name)

        await self.channel_layer.group_add(
            'driver', self.channel_name
        )

        await self.send({
            'type': 'websocket.accept'
        })

    async def websocket_receive(self, event):
        print("recived ", event)

        await self.channel_layer.group_send('driver', {
            'type': 'chat.message',
            'message': event['text']
        })


    async def chat_message(self, event):
        # print('chat', event)
        await self.send({
            'type': 'websocket.send',
            'text': event['message']
        })


    async def websocket_disconnect(self, event):
        print("dic connected", event, self.channel_layer, self.channel_name)

        await self.channel_layer.group_discard('driver', self.channel_name)
        raise StopConsumer()
    


# from masters.serializers import *
# from masters.models import *

# class UpdateModelChange(GenericAsyncAPIConsumer):
#     queryset = Status.objects.all()
#     serializer_class = StatusSerializer
#     permissions = (permissions.AllowAny,)

#     async def connect(self, **kwargs):  
#         print("connected")      
#         await self.model_change.subscribe()
#         # await super().connect()
#         await self.accept()

#     @model_observer(Status)
#     async def model_change(self, message, observer=None, **kwargs):
#         print("model sending message")
#         await self.send_json(message)

#     @model_change.serializer
#     def model_serialize(self, instance, action, **kwargs):
#         print("model change")
#         return dict(data=StatusSerializer(instance=instance).data, action=action.value)



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
    # return {
    #     'id': status_obj.id,
    #     # Add more fields here
    # }

