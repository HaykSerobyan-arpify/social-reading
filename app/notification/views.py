from rest_framework import serializers
from rest_framework import viewsets
from app.settings import DATETIME_FORMAT
from quotes.views import QuoteDetailSerializer
from register.views import UserFieldSerializer
from .models import Notification
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend


class NotificationSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(read_only=True, format=DATETIME_FORMAT, input_formats=None)

    user = UserFieldSerializer
    post = QuoteDetailSerializer(read_only=True)
    sender = UserFieldSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = ('id', 'user', 'post', 'sender', 'notification_type',
                  'text_preview', 'date', 'is_seen', 'is_open')


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class NotificationFilter(filters.FilterSet):
    user = CharFilterInFilter(field_name='user', lookup_expr='in')
    type = CharFilterInFilter(field_name='notification_type', lookup_expr='in')
    is_seen = CharFilterInFilter(field_name='is_seen', lookup_expr='in')

    class META:
        model = NotificationSerializer
        fields = ('user',)


class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = NotificationFilter
