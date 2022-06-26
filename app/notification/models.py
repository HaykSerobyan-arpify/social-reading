from django.db import models
from django.contrib.auth import get_user_model
from quotes.models import Quote


# Create your models here.

class Notification(models.Model):
    User = get_user_model()
    NOTIFICATION_TYPES = ((1, 'Like'), (2, 'Save'), (3, 'Comment'), (4, 'Upload'))

    post = models.ForeignKey(Quote, on_delete=models.CASCADE, related_name='noti_post', blank=True, null=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='noti_from_user')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='noti_to_user')
    notification_type = models.IntegerField(choices=NOTIFICATION_TYPES)
    text_preview = models.CharField(max_length=90, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.notification_type}|{self.user.first_name}|{self.is_seen}'
