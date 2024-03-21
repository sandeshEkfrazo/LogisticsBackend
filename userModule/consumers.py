from channels.consumer import SyncConsumer, AsyncConsumer
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
import json
from asgiref.sync import async_to_sync
from djangochannelsrestframework.mixins import ListModelMixin
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from django.contrib.auth.models import User
from .models import *
from .serializers import *
from djangochannelsrestframework.observer import model_observer
from djangochannelsrestframework import permissions


class PostConsumer(GenericAsyncAPIConsumer):

    queryset = ScheduledOrder.objects.all()
    serializer_class = ScheduledOrderSerializer
    permissions = (permissions.AllowAny,)

    async def connect(self, **kwargs):
        await self.model_change.subscribe()
        await super().connect()

    @model_observer(ScheduledOrder)
    async def model_change(self, message, observer=None, **kwargs):
        await self.send_json(message)

    @model_change.serializer
    def model_serialize(self, instance, action, **kwargs):
        return dict(data=ScheduledOrderSerializer(instance=instance).data, action=action.value)