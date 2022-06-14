from rest_framework import serializers
from rest_framework import viewsets
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'author', 'title', 'category', 'publisher', 'publish_date',)


class BookViewSet(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    queryset = Book.objects.all()
