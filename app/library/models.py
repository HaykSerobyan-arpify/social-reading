from django.core.validators import MinLengthValidator
from django.db import models
from categories.models import Category


class Sentence(models.Model):
    index_name = models.CharField('author', max_length=50,
                                  validators=[MinLengthValidator(limit_value=2, message=None), ])
    text = models.TextField('Text')

    def __str__(self):
        return self.text


class Book(models.Model):
    author = models.CharField('author', max_length=50,
                              validators=[MinLengthValidator(limit_value=2, message=None), ])
    title = models.CharField('title', max_length=50,
                             validators=[MinLengthValidator(limit_value=2, message=None), ])
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    publish_date = models.DateField()
    publisher = models.CharField('Publisher', max_length=50,
                                 validators=[MinLengthValidator(limit_value=2, message=None)])
    content = models.ManyToManyField('Sentence', blank=True)

    def __str__(self):
        return f'{self.author} | {self.title}'
