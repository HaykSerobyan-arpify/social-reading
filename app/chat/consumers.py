import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.core.serializers import serialize
from app.settings import MONGO_URI
import pymongo
from notification.models import Notification
from pprint import pprint

client = pymongo.MongoClient(MONGO_URI)
db = client.social
notify = dict()


class ChatConsumer(WebsocketConsumer):

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
            notify[str(author_id)] = serialize('json', Notification.objects.filter(user_id=author_id))
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'all_notifications',
                    'message': 'Like, Save, Comment Notifications',
                }
            )
        elif text_data_json['type'] == 'reply':
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
            # sender = text_data_json['sender']
            # post_id = text_data_json['post_id']
            category = text_data_json['category']

            for el in Notification.objects.filter(notification_type='upload'):
                if el.text_preview == category:
                    notify[str(el.user_id)] = serialize('json', Notification.objects.filter(user_id=el.user_id))

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
