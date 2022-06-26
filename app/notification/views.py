from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from notification.models import Notification


# Create your views here.
def showNotifications(request):
    user = request.user
    notification = Notification.objects.all()
    print(user)

    # template = loader.get_template('notification/notifications.html')

    context = {
        'notifications': notification,
    }
    return render(request, 'notification/notifications.html', context)
