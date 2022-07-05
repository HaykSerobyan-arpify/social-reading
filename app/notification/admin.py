from django.contrib import admin
from notification.models import Notification, OnlineUsers

admin.site.register(Notification)
admin.site.register(OnlineUsers)
