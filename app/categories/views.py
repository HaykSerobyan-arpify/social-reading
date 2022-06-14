from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers
from rest_framework import viewsets
from .models import Category
from django_filters import rest_framework as filters


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class CategoryFilter(filters.FilterSet):
    users = CharFilterInFilter(field_name='users', lookup_expr='in')

    class META:
        model = Category
        fields = ('users',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        # verbose_name_plural = 'Categories'
        model = Category
        fields = ('id', 'name', 'users')


class CategoriesViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CategoryFilter
