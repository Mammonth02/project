from audioop import reverse
from re import template
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

from django.contrib.auth.models import User

class Chat(models.Model):
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='sender', null=True)
    recipient = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='recipientc', null=True)
    text = models.TextField()
    time_create = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.text}'

    class Meta:
            verbose_name_plural = 'Coобшения'
            verbose_name= 'Сообшение    '