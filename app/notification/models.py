from django.db import models
from django.contrib.auth import get_user_model
from quotes.models import Quote

User = get_user_model()


# Create your models here.

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('like', 'Like'),
        ('save', 'Save'),
        ('comment', 'Comment'),
        ('reply', 'Comment Answer'),
        ('upload', 'Upload'),
    )

    post = models.ForeignKey(Quote, on_delete=models.CASCADE, related_name='noti_post', blank=True, null=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='noti_from_user')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='noti_to_user')
    notification_type = models.CharField(max_length=10, choices=NOTIFICATION_TYPES)
    text_preview = models.CharField(max_length=90, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.notification_type}|{self.user.first_name}|{self.is_seen}'


class OnlineUsers(models.Model):
    online = models.ManyToManyField(to=User, blank=True)

    def get_online_count(self):
        return self.online.count()

    def join(self, user):
        self.online.add(user)
        self.save()

    def leave(self, user):
        self.online.remove(user)
        self.save()

    def __str__(self):
        return f"{self.name} ({self.get_online_count()})"
