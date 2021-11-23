from django.contrib.auth import get_user_model
from django.db import models

from core.choices import StatusTicket


class Ticket(models.Model):
    author = models.ForeignKey(get_user_model(), related_name='tickets', on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    status = models.CharField(max_length=1, choices=StatusTicket.choices, default='O')
    created = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    ticket = models.ForeignKey(Ticket, related_name='messages', on_delete=models.CASCADE)
    author = models.ForeignKey(get_user_model(), related_name='messages', on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
