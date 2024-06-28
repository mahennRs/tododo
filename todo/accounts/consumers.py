from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
import json

class TodoConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.user = await self.get_user_by_scope()
        
        if not self.user.is_authenticated:
            await self.close()
            return

        self.group_name = str(self.user.id)
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'todo_message',
                'message': message
            }
        )

    async def todo_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({'message': message}))

    @database_sync_to_async
    def get_user_by_scope(self):
        user_id = self.scope['user'].id
        if user_id:
            return User.objects.get(id=user_id)
        return None
