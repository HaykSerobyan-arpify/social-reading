from django.db import models
from quotes.models import Quote
from register.models import User


class Like(models.Model):
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} | {self.like}'
