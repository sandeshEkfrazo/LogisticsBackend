from channels.consumer import AsyncConsumer
from channels.exceptions import StopConsumer

class DriverNotificationConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print('web socket connected')
        await self.send({
            'type': 'websocket.accept'
        })

    async def websocket_receive(self, event):
        print('web socket recived')
        await self.send({
            'type': 'websocket.send',
            'text': "messge sent"
        })