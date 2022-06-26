from django.db import models
from quotes.models import Quote
from register.models import User
from django.db.models.signals import post_save, post_delete
from notification.models import Notification


class Like(models.Model):
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} | {self.like}'

    def user_liked_quote(self, instance, *args, **kwargs):
        like = instance
        post = like.quote
        sender = like.user

        notify = Notification(post=post, sender=sender, user=self.quote.author, notification_type=1)
        notify.save()

    def user_unliked_quote(self, instance, *args, **kwargs):
        like = instance
        post = like.quote
        sender = like.user

        notify = Notification.objects.filter(post=post, sender=sender, notification_type=1)
        notify.delete()


post_save.connect(Like.user_liked_quote, sender=Like)
post_delete.connect(Like.user_unliked_quote, sender=Like)
