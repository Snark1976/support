from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail, mail_admins

from core.models import Ticket, Message


@shared_task
def send_mail_created_ticket(ticket):
    user = get_user_model().objects.get(pk=ticket['author'])
    send_mail(
        'Your ticket has been registered',
        f'Dear, {user.username}.\n'
        f'Your ticket is registered under the number {ticket["id"]}.\n'
        f'Ticket text: "{ticket["text"]}"\n'
        f'Time registration: {ticket["created"]}',
        'support@example.com',
        [user.email],
        fail_silently=False,
    )
    mail_admins(
        'New ticket',
        f'User: {user.username}, ID: {ticket["author"]}.\n, ticket ID: {ticket["id"]}.\n'
        f'Ticket text: "{ticket["text"]}"\n'
        f'Time registration: {ticket["created"]}',
        fail_silently=False,
    )
    return True


@shared_task
def send_mail_change_status_ticket(ticket_id):
    ticket = Ticket.objects.get(pk=int(ticket_id))
    send_mail(
        'Your ticket status has been changed',
        f'Dear, {ticket.author}.\n'
        f'The status of your ticket "{ticket.text}" has been changed to "{ticket.status}".\n'
        f'Ticket ID: {ticket.pk}.\n',
        'support@example.com',
        [ticket.author.email],
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
        f'Total messages: {len(Message.objects.all())}',
        fail_silently=False,
    )
    return True
