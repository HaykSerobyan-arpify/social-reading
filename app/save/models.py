from django.db import models
from quotes.models import Quote
from register.models import User


class Save(models.Model):
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, related_name="save_users")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
