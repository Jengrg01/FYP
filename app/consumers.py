import json
from channels.generic.websocket import AsyncWebsocketConsumer
from user.models import ChatRoom, Message
from .models import Notification, Makeup
from django.contrib.auth.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f"chat_{self.room_id}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        sender_id = data['sender_id']

        await self.save_message(room_id=self.room_id, sender_id=sender_id, message=message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender_id': sender_id
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps(event))

    @staticmethod
    async def save_message(room_id, sender_id, message):
        sender = await User.objects.aget(id=sender_id)
        room = await ChatRoom.objects.aget(id=room_id)
        artist = room.artist

        await Message.objects.acreate(room=room, sender=sender, content=message)

        if sender.id != artist.user.id:
            await Notification.objects.acreate(
                artist=artist,
                message=f"You have a new message from {sender.username}",
                is_read=False
            )
