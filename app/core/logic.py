from core.models import Ticket


def get_user_tickets(user):
    if user.is_staff:
        return Ticket.objects.all()
    else:
        return Ticket.objects.filter(author_id=user.id)
