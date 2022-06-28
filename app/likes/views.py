from rest_framework import serializers
from rest_framework import viewsets

from register.views import UserFieldSerializer
from .models import Like


class LikeSerializer(serializers.ModelSerializer):
    user = UserFieldSerializer(read_only=True)

    class Meta:
        model = Like
        fields = ('quote', 'like')


class LikeViewSet(viewsets.ModelViewSet):
    serializer_class = LikeSerializer
    queryset = Like.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
