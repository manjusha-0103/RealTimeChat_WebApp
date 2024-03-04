import json

# from django.contrib.auth.models import User
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async, async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model
User = get_user_model()
from django.core.serializers.json import DjangoJSONEncoder

from .models import Teams, Messages

class ChatConsumer(AsyncWebsocketConsumer):
    connected_members = set()
    async def connect(self):
        print("user",self.scope["user"])
        user = self.scope["user"]

        print(user.photo)
        

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        if not await self.is_user_in_team():
            await self.add_user_to_team()
            print("added user")
        print("already a member")

        if user not in self.connected_members:
            self.connected_members.add(user)
        
        
        await self.accept()

        channel_layer = get_channel_layer()
        
        await channel_layer.send(self.room_group_name,{
            'type': 'user.joined',
            'username': self.scope['user'].username,
            'members': list(self.connected_members),
        })

        # await self.channel_layer.group_send(
        #     self.room_group_name,
            
        # )




    # Asynchronous methods for checking and adding user to team
    async def is_user_in_team(self):
        """Asynchronously checks if the user is already a member of the team."""
        return async_to_sync( Teams.objects.filter(room_name=self.room_name, members__username=self.scope['user']).exists)

    async def add_user_to_team(self):
        """Asynchronously adds the user to the team if not already a member."""
        team = await async_to_sync(Teams.objects.get, room_name=self.room_name)
        await async_to_sync(team.members.add, User.objects.get(username=self.scope['user']))

    # async def disconnect(self):
    #     await self.channel_layer.group_discard(
    #         self.room_group_name,
    #         # self.channel_name
    #     )
        
    async def disconnect(self,close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # async def getallmembers(self):
    #     members = async_to_sync(Teams.objects.get(room_name=self.room_name))

    # Receive message from WebSocket
    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        user = self.scope['user']
        
        print(data)
        message = data['message']
        username = data['username']
        room = data['room']
        # photo = data['photo']

        
        

        # message_id = await self.save_message(username, room, message,user)
        await self.save_message(username, room, message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'room':room ,
                # 'photo': photo
                
                # 'message_id' : message_id
            }
        )

    @sync_to_async
    def serialize_photo(self, obj):
        if obj:
            return str(obj)
        return None

    # Receive message from room group
    async def chat_message(self, event):

        print(event)


        message = event['message']
        username = event['username']
        room = event['room']
        user = await self.findUser(username)
        photo = str(user.photo.url) if user.photo else ""

        

        # message_id = await self.save_message(username, event['room'], message)

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            # 'user' : user,
            "room" : room,
            'photo': photo

        }, cls=DjangoJSONEncoder))

        # await self.connect()

    @sync_to_async
    def save_message(self, username, room, message):
        user = User.objects.get(username=username)
        room = Teams.objects.get(slug=room)

        Messages.objects.create(user=user, room=room, content=message)
        # message=Messages.objects.create(user=user, room=room, content=message)
        # return message.id
    @sync_to_async
    def findUser(self,username):
        user = User.objects.get(username=username)

        return user