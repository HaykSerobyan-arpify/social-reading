import uuid
from django.core.validators import MinLengthValidator, validate_image_file_extension, FileExtensionValidator
from django.db import models
from register.models import User


class Quote(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    published = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    author = models.ForeignKey(User, related_name='author', on_delete=models.CASCADE, verbose_name='Quote author')

    book_author = models.CharField('Book author', max_length=20, blank=True,
                                   validators=[MinLengthValidator(limit_value=2, message=None), ])

    quote_title = models.CharField('Quote Title', max_length=20, blank=True,
                                   validators=[MinLengthValidator(limit_value=2, message=None), ])

    book_category = models.CharField('Category', max_length=20,
                                     validators=[MinLengthValidator(limit_value=2, message=None), ])

    quote_file = models.ImageField('Quote', upload_to='upload',
                                   validators=[validate_image_file_extension,
                                               FileExtensionValidator(allowed_extensions=['jpeg', 'png', 'jpg'])], )

    quote_opencv_file = models.ImageField('Changed photo', upload_to='opencv',
                                          validators=[validate_image_file_extension,
                                                      FileExtensionValidator(
                                                          allowed_extensions=['jpeg', 'png', 'jpg'])],
                                          blank=True, null=True)

    quote_text = models.TextField('Quote text', blank=True, null=True)

    quote_text_json = models.JSONField('JSON text', blank=True, null=True)

    percent = models.FloatField('Percent', blank=True, null=True)

    text_background = models.ImageField('Quote text background', upload_to='upload',
                                        validators=[validate_image_file_extension,
                                                    FileExtensionValidator(allowed_extensions=['jpeg', 'png', 'jpg'])],
                                        null=True, blank=True)

    styles = models.JSONField(blank=True, null=True)

    date_posted = models.DateTimeField(auto_now_add=True)

    def get_comments(self):
        return self.comments.filter(parent=None)

    def __str__(self):
        return f'Author: {self.book_author} | ' \
               f'Title: {self.quote_title} | ' \
               f'Category: {self.book_category} | ' \
               f'User: {self.author}' \
               f'Date posted: {self.date_posted}'
