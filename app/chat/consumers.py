import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer, WebsocketConsumer
from django.core.serializers import serialize

from django.http import JsonResponse
from rest_framework.response import Response
from app.settings import MONGO_URI
import pymongo
from chat.models import Conversation
from notification.models import Notification
from quotes.models import Quote
from register.models import User
from pprint import pprint

client = pymongo.MongoClient(MONGO_URI)
db = client.social
notify = dict()


class ChatConsumer(WebsocketConsumer):
    # """
    # This consumer is used to show user's online status,
    # and send notifications.
    # """
    #
    # def __init__(self, *args, **kwargs):
    #    super().__init__(args, kwargs)
    #    self.room_name = None
    #
    # def connect(self):
    #    print("Connected!")
    #    self.room_name = "online"
    #    # print(self.scope)
    #    self.accept()
    #
    #    self.send_json(
    #        {
    #            "type": "welcome_message",
    #            "notifications": "asenq te barev",
    #        }
    #    )
    #
    # def disconnect(self, code):
    #    print("Disconnected!")
    #    return super().disconnect(code)
    #
    # def receive_json(self, content, **kwargs):
    #    notifications = dict()
    #    online_users = db['chat_conversation_online'].find({})
    #
    #    # print(content)
    #
    #    message_type = content["type"]
    #    if message_type == "login":
    #        print(content)
    #        Conversation.objects.get(name='OnlineUsers').join(content['user_id'])
    #        print(Conversation.objects.get(name='OnlineUsers'))
    #
    #    elif message_type == "logout":
    #        print(content)
    #        Conversation.objects.get(name='OnlineUsers').leave(content['user_id'])
    #        print(Conversation.objects.get(name='OnlineUsers'))
    #
    #    if message_type == "like":
    #        print("Online users", online_users)
    #        for el in online_users:
    #            print("For ------", el['user_id'])
    #            notifications[el['user_id']] = serialize('json', Notification.objects.filter(user=el['user_id']),
    #                                                     ensure_ascii=False)
    #        print(notifications)
    #
    #        self.send_json({
    #            "type": "like_response",
    #            "message": 'I see your like and add it ...',
    #            "online_users_notification": notifications,
    #        })
    #
    #    elif message_type == "call":
    #
    #        self.send_json({
    #            "type": "call_response",
    #            "notifications": notifications,
    #        })
    #
    #    return super().receive_json(content, **kwargs)
    #

    online_users = db['chat_conversation_online'].find({})

    def connect(self):
        self.room_name = 'online'
        self.room_group_name = 'users'

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        if text_data_json['type'] in ['like', 'save', 'comment']:
            author_id = text_data_json['author_id']
            print(text_data_json)
            notify[str(author_id)] = serialize('json', Notification.objects.filter(user_id=author_id))
            print(notify)
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'all_notifications',
                    'message': 'Like, Save, Comment Notifications',
                }
            )
        elif text_data_json['type'] == 'reply':
            print(text_data_json)
            author_id = text_data_json['author_id']
            parent_user_id = text_data_json['parent_user_id']
            notify[str(author_id)] = serialize('json', Notification.objects.filter(user_id=author_id))
            notify[str(parent_user_id)] = serialize('json', Notification.objects.filter(user_id=parent_user_id))
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'all_notifications',
                    'message': 'Reply Notification',
                }
            )
        elif text_data_json['type'] == 'upload':
            print(text_data_json)
            sender = text_data_json['sender']
            post_id = text_data_json['post_id']
            category = text_data_json['category']
            print("--------------------")
            for el in Notification.objects.filter(notification_type='upload'):
                print(el.sender_id)
                print(el.text_preview)
                if el.text_preview == category:
                    notify[str(el.user_id)] = serialize('json', Notification.objects.filter(user_id=el.user_id))

            pprint(notify)
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'all_notifications',
                    'message': 'Upload Notification',
                }
            )

    # Receive message from room group
    def all_notifications(self, *args):
        self.send(text_data=json.dumps({
            'room_group_name': self.room_group_name,
            'self.channel_name': self.channel_name,
            'type': 'notifications',
            'all': notify,
        }))
