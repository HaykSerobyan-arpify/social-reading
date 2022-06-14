from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers
from rest_framework import viewsets
from django_filters import rest_framework as filters
from register.views import UserFieldSerializer
from .models import Save


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class SaveFilter(filters.FilterSet):
    id = CharFilterInFilter(field_name='user', lookup_expr='in')

    class META:
        model = Save
        fields = ('user',)


class SaveSerializer(serializers.ModelSerializer):
    user = UserFieldSerializer(read_only=True)

    class Meta:
        model = Save
        fields = ('id', 'quote', 'user')


class SaveViewSet(viewsets.ModelViewSet):
    serializer_class = SaveSerializer
    queryset = Save.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = SaveFilter

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
