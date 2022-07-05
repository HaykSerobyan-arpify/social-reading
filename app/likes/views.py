import pymongo
from rest_framework import serializers, status
from rest_framework import viewsets
from django.core.serializers import serialize
from app.settings import MONGO_URI
from chat.consumers import ChatConsumer
from register.models import User
from rest_framework.response import Response
from notification.models import Notification
from quotes.models import Quote
from register.views import UserFieldSerializer
from .models import Like


class LikeSerializer(serializers.ModelSerializer):
    user = UserFieldSerializer(read_only=True)

    class Meta:
        model = Like
        fields = ('id', 'quote', 'user')


class LikeViewSet(viewsets.ModelViewSet):
    serializer_class = LikeSerializer
    queryset = Like.objects.all()

    def perform_create(self, serializer):
        if self.request.data.get('user_id') != self.request.user.id:
            Notification.objects.create(
                post=Quote.objects.get(id=self.request.data.get('quote')),
                sender=self.request.user,
                user=User.objects.get(id=self.request.data.get('user_id')),
                notification_type='like',
            )

        serializer.save(user=self.request.user)
