from rest_framework.views import APIView
from .service import TextDetectionError
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
from notification.models import Notification
from quotes.models import Quote
from categories.models import Category
import pymongo
from app.settings import MONGO_URI, DATETIME_FORMAT
from django_filters.rest_framework import DjangoFilterBackend
from quotes.service import QuoteFilter, get_text_from_book, recognize_text, recognize_another_text
from django.contrib.auth.models import AnonymousUser
from app.settings import BACKEND_DOMAIN, DOMAIN
from register.models import User
from register.views import UserSerializer
from save.views import SaveSerializer
from django.core.exceptions import FieldError
import requests
from pprint import pprint
import json


def coming_soon(request):
    return render(request, 'quotes/coming_soon.html', {'backend_url': BACKEND_DOMAIN})


class ShareQuote(APIView):
    def get(self, request, *args, **kwargs):
        post_id = self.kwargs['pk']
        resp = requests.get(f'https://www.sr-be.arpify.com/quotes/{post_id}')
        post = json.loads(resp.text)

        # return render(request, "quotes/home.html", {'url': f'https://d7cb-31-47-198-190.eu.ngrok.io/share/{post_id}',
        #                                             'post': post})

        return render(request, 'quotes/share_view.html', {'post': post,
                                                          'url': f'https://www.sr-be.arpify.com/share/{post_id}',
                                                          'color': json.loads(post['styles']).get('color'),
                                                          'background': json.loads(post['styles']).get('background'),
                                                          'font': json.loads(post['styles']).get('font'),
                                                          'size': json.loads(post['styles']).get('size'),
                                                          'likes_count': len(post.get('likes')),
                                                          'comments_count': len(post.get('comments')),
                                                          'front_url': DOMAIN})


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
        fields = ('id', 'author', 'date_posted', 'language', 'text',
                  'book_author', 'quote_title', 'book_category',
                  'quote_file', 'quote_opencv_file', 'quote_text', 'quote_text_json',
                  'percent', 'styles', 'text_background', 'likes',
                  'save_users', 'comments', 'published', 'is_active')


class QuoteDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quote
        fields = ('id', 'book_author', 'quote_title', 'quote_text',
                  'quote_text_json', 'percent', 'styles', 'text_background')


class QuotesViewSet(viewsets.ModelViewSet):
    serializer_class = QuoteSerializer
    queryset = Quote.objects.all().order_by('-date_posted')
    filter_backends = (DjangoFilterBackend,)
    filterset_class = QuoteFilter

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        another_users_id = set()
        if self.request.data.get('published'):
            for post in Quote.objects.filter(book_category=serializer.data.get('book_category')):
                if self.request.user.id != post.author.id:
                    another_users_id.add(post.author.id)

            for user_id in another_users_id:
                # create Notifications for all users by this category
                # we can change it by book name later . . . . . . . . . . ! ! ! ! ! ! ! ! ! ! ! ! ! ! ! !
                Notification.objects.create(
                    post=Quote.objects.get(id=instance.id),
                    sender=self.request.user,
                    user=User.objects.get(id=user_id),
                    notification_type='upload',
                    text_preview=serializer.data.get('book_category'),
                )

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        if len(self.request.data.get('text')) == 0 and len(self.request.data.get('quote_file')) > 0:

            if self.request.data.get('language') != 'eng':
                text = recognize_another_text(self.request.data.get('quote_file'), self.request.data.get('language'))

                serializer.save(author=self.request.user,
                                book_author=self.request.data.get('book_author'),
                                quote_title=self.request.data.get('quote_title'),
                                quote_text=text,
                                percent=0,
                                book_category=self.request.data.get('book_category'))

            if self.request.data.get('language') == 'eng':

                # text recognition from Holy Bible
                try:
                    recognized_array = recognize_text(self.request.data.get('quote_file'))
                    quote_text, text_JSON, percent, author, title, category = get_text_from_book(recognized_array)

                    try:
                        # test
                        if isinstance(self.request.user, AnonymousUser):
                            serializer.save(author=None, book_author=author, quote_title=title,
                                            quote_text=quote_text, percent=percent, book_category=category,
                                            quote_text_json=text_JSON,
                                            quote_opencv_file=f"opencv/{self.request.data.get('quote_file')}")
                        else:
                            serializer.save(author=self.request.user, book_author=author, quote_title=title,
                                            quote_text=quote_text, percent=percent, book_category=category,
                                            quote_text_json=text_JSON,
                                            quote_opencv_file=f"opencv/{self.request.data.get('quote_file')}")
                    except ValueError:
                        raise FieldError("User must be authorised")

                    for post in Quote.objects.filter(book_category=category):

                        if self.request.user.id != post.author.id:
                            Notification.objects.create(
                                post=post,
                                sender=self.request.user,
                                user=User.objects.get(id=post.author.id),
                                notification_type='upload',
                                text_preview=category,
                            )
                except TextDetectionError:

                    text = recognize_another_text(self.request.data.get('quote_file'))

                    serializer.save(author=self.request.user,
                                    book_author=self.request.data.get('book_author'),
                                    quote_title=self.request.data.get('quote_title'),
                                    quote_text=text,
                                    percent=0,
                                    book_category=self.request.data.get('book_category'))

        elif len(self.request.data.get('text')) == 0 and len(self.request.data.get('quote_file')) == 0:
            raise FieldError("Please choose TEXT or QUOTE FILE")
        else:
            # Later here should be the logic to search from google
            book_author = self.request.data.get('book_author')
            quote_title = self.request.data.get('quote_title')
            quote_text = self.request.data.get('text')
            category = self.request.data.get('book_category')

            serializer.save(author=self.request.user,
                            book_author=book_author,
                            quote_title=quote_title,
                            quote_text=quote_text,
                            percent=0,
                            book_category=category)

    def get_success_headers(self, data):
        client = pymongo.MongoClient(MONGO_URI)
        db = client.social
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
