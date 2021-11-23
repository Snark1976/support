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
def send_mail_added_message(author_id, message_id):
    author_message = get_user_model().objects.get(pk=int(author_id))
    message = Message.objects.get(pk=int(message_id))
    author_ticket = get_user_model().objects.get(pk=message.ticket.author.id)
    print(author_message, author_ticket, message)
    send_mail(
        'Message added to your ticket',
        f'Dear, {author_ticket.username}.\n'
        f'The message "{message.text}" has been added to your ticket "{message.ticket.text}".\n'
        f'Author message: "{author_message.username}"\n'
        f'Ticket ID: "{message.ticket.id}"\n'
        f'Time: {message.created}',
        'support@example.com',
        [author_ticket.email],
        fail_silently=False,
    )
    mail_admins(
        'New message',
        f'Ticket ID: {message.ticket.id}"\n'
        f'New message: "{message.ticket.text}"\n'
        f'Author of the message: {author_message.username}, ID: {author_id}\n'
        f'Time: {message.created}',
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
