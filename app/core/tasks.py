from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail, mail_admins

from core.models import Ticket, Message


@shared_task
def send_mail_created_ticket(user_id, ticket_id, title, text, time):
    user = get_user_model().objects.get(id=user_id)
    send_mail(
        'Your ticket has been registered',
        f'Dear, {user.username}.\n'
        f'Your ticket is registered under the number {ticket_id}.\n'
        f'Title: "{title}"\n'
        f'Text: "{text}"\n'
        f'Time registration: {time}',
        'support@example.com',
        [user.email],
        fail_silently=False,
    )
    mail_admins(
        'New ticket',
        f'User: {user.username}, ID: {user_id}.\n, ticket ID: {ticket_id}.\n'
        f'Title: "{title}"\n'
        f'Text: "{text}"\n'
        f'Time registration: {time}',
        fail_silently=False,
    )
    return True


@shared_task
def send_mail_change_status_ticket(user_id, ticket_id, title, status):
    user = get_user_model().objects.get(id=user_id)
    send_mail(
        'Your ticket status has been changed',
        f'Dear, {user.username}.\n'
        f'The status of your ticket "{title}" has been changed to "{status}".\n'
        f'Ticket ID: {ticket_id}.\n',
        'support@example.com',
        [user.email],
        fail_silently=False,
    )


@shared_task
def send_mail_added_message(author_message_id, author_ticket_id, ticket_id, title, text, time):
    user = get_user_model().objects.get(id=author_ticket_id)
    if author_message_id == author_ticket_id:
        author_message = user
    else:
        author_message = get_user_model().objects.get(id=author_message_id)
    send_mail(
        'Message added to your ticket',
        f'Dear, {user.username}.\n'
        f'The message "{text}" has been added to your ticket {title}.\n'
        f'Author message: "{author_message.username}"\n'
        f'Ticket ID: "{ticket_id}"\n'
        f'Time: {time}',
        'support@example.com',
        [user.email],
        fail_silently=False,
    )
    mail_admins(
        'New message',
        f'Ticket ID: {ticket_id}, title: "{title}"\n'
        f'User: {user.username}, user ID: {author_ticket_id}\n'
        f'New message: "{text}"\n'
        f'Author of the message: {author_message.username}, ID: {author_message_id}\n'
        f'Time: {time}',
        fail_silently=False,
    )
    return True


@shared_task
def send_email_report():
    mail_admins(
        'Report support',
        f'Total tickets: {len(Ticket.objects.all())}\n'
        f'Total messages: {len(Message.objects.all())}\n'
        f'Opened tickets: ',
        fail_silently=False,
    )
    return True
