from django.contrib.auth import get_user_model
from django.db import models

STATUS_TICKET = (
    ('O', 'Opened '),
    ('H', 'On Hold'),
    ('R', 'Awaiting Reply'),
    ('C', 'Completed'),
)


class Ticket(models.Model):
    title_ticket = models.CharField(max_length=200)
    status_ticket = models.CharField(max_length=1, choices=STATUS_TICKET, default='O')
    author = models.ForeignKey(get_user_model(), related_name='tickets', on_delete=models.CASCADE)


class Message(models.Model):
    ticket = models.ForeignKey(Ticket, related_name='messages', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    author = models.ForeignKey(get_user_model(), related_name='messages', on_delete=models.CASCADE)

