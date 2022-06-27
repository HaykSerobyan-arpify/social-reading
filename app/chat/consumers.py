from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer

from chat.models import Conversation


class ChatConsumer(JsonWebsocketConsumer):
    """
    This consumer is used to show user's online status,
    and send notifications.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.user = None
        self.conversation_name = None
        self.conversation = None

    def connect(self):
        print("Connected!")
        self.user = self.scope["user"]
        if not self.user.is_authenticated:
            return

        self.accept()
        self.conversation_name = f"{self.scope['url_route']['kwargs']['conversation_name']}"
        self.conversation, created = Conversation.objects.get_or_create(name=self.conversation_name)

        async_to_sync(self.channel_layer.group_add)(
            self.conversation_name,
            self.channel_name,
        )

        self.send_json(
            {
                "type": "welcome_message",
                "message": "Hey there! You've successfully connected!",
            }
        )

    def disconnect(self, code):
        print("Disconnected!")
        return super().disconnect(code)

    def receive_json(self, content, **kwargs):
        self.send_json({
            "type": "response",
            "message": "Django receive your message ?",
        })
        message_type = content["type"]
        if message_type == "chat_message":
            print(content)
            async_to_sync(self.channel_layer.group_send)(
                self.room_name,
                {
                    "type": "chat_message_echo",
                    "name": content["name"],
                    "message": content["message"],
                },
            )
        if message_type == "greeting":
            async_to_sync(self.channel_layer.group_send)(
                self.room_name,
                {
                    "type": "greeting_response_echo",
                    "name": "DJANGO",
                    "message": "How are you?",
                },
            )
            print(content)
            print(content["message"])
        elif message_type == "Like":
            async_to_sync(self.channel_layer.group_send)(
                self.room_name,
                {
                    "type": "like_response_echo",
                    "name": "DJANGO",
                    "message": "I see your like !!!",
                },
            )
            print(content)
            print('LIKE logic')
        elif message_type == "Save":
            async_to_sync(self.channel_layer.group_send)(
                self.room_name,
                {
                    "type": "save_response_echo",
                    "name": "DJANGO",
                    "message": "I see your save post !!!",
                },
            )
            print(content)
            print('SAVE logic')
        elif message_type == "Comment":
            async_to_sync(self.channel_layer.group_send)(
                self.room_name,
                {
                    "type": "comment_response_echo",
                    "name": "DJANGO",
                    "message": "I see your comment !!!",
                },
            )
            print(content)
            print('COMMENT logic')
        elif message_type == "Upload":
            async_to_sync(self.channel_layer.group_send)(
                self.room_name,
                {
                    "type": "upload_response_echo",
                    "name": "DJANGO",
                    "message": "I see that you add post with this category . . . !!!",
                },
            )
            print(content)
            print('UPLOAD logic')
        return super().receive_json(content, **kwargs)

    def chat_message_echo(self, event):
        self.send_json(event)

    def greeting_response_echo(self, event):
        self.send_json(event)

    def like_response_echo(self, event):
        self.send_json(event)

    def save_response_echo(self, event):
        self.send_json(event)

    def comment_response_echo(self, event):
        self.send_json(event)

    def upload_response_echo(self, event):
        self.send_json(event)


NOTIFICATION_TYPES = ((1, 'Like'), (2, 'Save'), (3, 'Comment'), (4, 'Upload'))


class NotificationConsumer(JsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.user = None
        self.notification_group_name = None

    def connect(self):
        self.user = self.scope["user"]
        if not self.user.is_authenticated:
            return

        self.accept()

        # private notification group
        self.notification_group_name = self.user.username + "__notifications"
        async_to_sync(self.channel_layer.group_add)(
            self.notification_group_name,
            self.channel_name,
        )

        # Send count of unread messages
        unread_count = Message.objects.filter(to_user=self.user, read=False).count()
        self.send_json(
            {
                "type": "unread_count",
                "unread_count": unread_count,
            }
        )

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.notification_group_name,
            self.channel_name,
        )
        return super().disconnect(code)

    def new_message_notification(self, event):
        self.send_json(event)

    def unread_count(self, event):
        self.send_json(event)
