from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.contrib.auth.models import User
# Create your models here.

class CustomUser(AbstractUser):
    icon = models.ImageField(null=False, blank=False, upload_to="media", default="media/default.jpg") 
    friends = models.ManyToManyField('self', blank=True)
    def __str__(self):
        return self.username


class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender.username} -> {self.recipient.username}: {self.content}'