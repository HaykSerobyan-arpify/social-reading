from django.db import models
from library.models import Book


class Sentence(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="sentences")
    index_name = models.CharField('IndexName', max_length=50)
    text = models.TextField('Text')

    def __str__(self):
        return f'{self.id}---{self.book}---{self.index_name}'
