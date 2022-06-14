from quotes.models import Quote
from register.models import User
from django.db import models


class Comment(models.Model):
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, related_name="comments", )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name="children")
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created', ]

    def get_comments(self):
        return Comment.objects.filter(parent=self).filter(active=True)

    def __str__(self):
        return f'{self.user} - {self.body}'
