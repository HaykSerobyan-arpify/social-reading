from rest_framework import viewsets
from rest_framework import serializers
from comments.models import Comment
from app.settings import DATETIME_FORMAT
from notification.models import Notification
from quotes.models import Quote
from register.views import UserFieldSerializer
from register.models import User


class FilterCommentListSerializer(serializers.ListSerializer):

    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class RecursiveSerializer(serializers.Serializer):

    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CommentsSerializer(serializers.ModelSerializer):
    user = UserFieldSerializer(read_only=True)
    parent = Comment
    children = RecursiveSerializer(many=True, required=False)
    created = serializers.DateTimeField(read_only=True, format=DATETIME_FORMAT, input_formats=None)
    updated = serializers.DateTimeField(read_only=True, format=DATETIME_FORMAT, input_formats=None)

    def get_text(self, obj):
        if obj.deleted:
            return None
        return obj.text

    class Meta:
        list_serializer_class = FilterCommentListSerializer
        model = Comment
        fields = ("id", "user", "quote", "body", "created", "updated", 'parent', "children")


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    queryset = Comment.objects.all()

    def perform_create(self, serializer):

        if self.request.user.id == self.request.data.get('post_author_id') and self.request.data.get(
                'parent_user_id') is not None:
            Notification.objects.create(
                post=Quote.objects.get(id=self.request.data.get('quote')),
                sender=self.request.user,
                user=User.objects.get(id=self.request.data.get('parent_user_id')),
                notification_type='reply',
                text_preview=self.request.data.get('body'),
            )

        if self.request.user.id != self.request.data.get('post_author_id') \
                and self.request.user.id != self.request.data.get('parent_user_id'):
            if self.request.data.get('parent_user_id') is None:
                Notification.objects.create(
                    post=Quote.objects.get(id=self.request.data.get('quote')),
                    sender=self.request.user,
                    user=User.objects.get(id=self.request.data.get('post_author_id')),
                    notification_type='comment',
                    text_preview=self.request.data.get('body'),
                )
            else:
                Notification.objects.create(
                    post=Quote.objects.get(id=self.request.data.get('quote')),
                    sender=self.request.user,
                    user=User.objects.get(id=self.request.data.get('parent_user_id')),
                    notification_type='reply',
                    text_preview=self.request.data.get('body'),
                )
                if self.request.data.get('post_author_id') != self.request.data.get('parent_user_id'):
                    Notification.objects.create(
                        post=Quote.objects.get(id=self.request.data.get('quote')),
                        sender=self.request.user,
                        user=User.objects.get(id=self.request.data.get('post_author_id')),
                        notification_type='comment',
                        text_preview=self.request.data.get('body'),
                    )

        serializer.save(user=self.request.user)
