from django.db import models
from quotes.models import Quote
from register.models import User
from django.db.models.signals import post_save, post_delete
from notification.models import Notification


class Like(models.Model):
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} | {self.quote}'

