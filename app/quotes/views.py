from django.core.exceptions import FieldError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from pymongo.errors import BulkWriteError
from rest_framework import serializers, status
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from comments.views import CommentsSerializer
from likes.views import LikeSerializer
from quotes.models import Quote
from categories.models import Category
import pymongo
from app.settings import MONGO_URI, DATETIME_FORMAT
from django_filters.rest_framework import DjangoFilterBackend
from quotes.service import QuoteFilter, get_text_from_book, recognize_text
from django.contrib.auth.models import AnonymousUser
from register.views import UserSerializer
from save.views import SaveSerializer


def coming_soon(request):
    return render(request, 'quotes/coming_soon.html')


def like_quote(request):
    quote = get_object_or_404(Quote, id=request.POST.get('quote_id'))
    if quote.likes.filter(id=request.user.id).exists():
        pass
    else:
        quote.likes.add(request.user)
    return HttpResponseRedirect(reverse('coming_soon'))


class QuoteSerializer(serializers.ModelSerializer):
    date_posted = serializers.DateTimeField(read_only=True, format=DATETIME_FORMAT, input_formats=None)
    author = UserSerializer(read_only=True)
    likes = LikeSerializer(many=True, read_only=True)
    save_users = SaveSerializer(many=True, read_only=True)
    comments = CommentsSerializer(many=True, read_only=True)

    class Meta:
        model = Quote
        fields = ('id', 'author', 'date_posted',
                  'book_author', 'quote_title', 'book_category',
                  'quote_file', 'quote_text', 'quote_text_json',
                  'percent', 'styles', 'text_background', 'likes',
                  'save_users', 'comments', 'published', 'is_active')


class QuotesViewSet(viewsets.ModelViewSet):
    serializer_class = QuoteSerializer
    queryset = Quote.objects.all().order_by('-date_posted')
    filter_backends = (DjangoFilterBackend,)
    filterset_class = QuoteFilter

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):

        # text recognition
        recognized_array = recognize_text(self.request.data.get('quote_file'))
        quote_text, text_JSON,  percent, author, title, category = get_text_from_book(recognized_array)
        try:
            # test
            if isinstance(self.request.user, AnonymousUser):
                serializer.save(author=None, book_author=author, quote_title=title,
                                quote_text=quote_text, percent=percent, book_category=category,
                                quote_text_json=text_JSON, quote_file=f"upload{self.request.data.get('quote_file')}")
            else:
                serializer.save(author=self.request.user, book_author=author, quote_title=title,
                                quote_text=quote_text, percent=percent, book_category=category,
                                quote_text_json=text_JSON, quote_file=f"upload/{self.request.data.get('quote_file')}")
        except ValueError:
            raise FieldError("User must be authorised")

    def get_success_headers(self, data):
        client = pymongo.MongoClient(MONGO_URI)
        db = client.social_reading_db
        category = data['book_category'].capitalize()
        user = self.request.user
        if db.categories_category.find_one({"name": category}) is None:
            new_category = Category.objects.create(name=category)
            new_category.users.add(user)
        else:
            cat = Category.objects.get(name=category)
            try:
                cat.users.add(self.request.user)
            except BulkWriteError:
                # if user exists in category users
                pass
            except Exception:
                # if user exists in category users
                pass


class PublishQuotesViewSet(viewsets.ModelViewSet):
    serializer_class = QuoteSerializer
    queryset = Quote.objects.filter(published=True)
