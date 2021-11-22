from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.serializers import TicketSerializer, MessageSerializer, TicketsViewSerializer
from core.models import Ticket
from core.permissions import PermissionToOneTicketView
from core.tasks import send_mail_created_ticket, send_mail_change_status_ticket, send_mail_added_message


class TicketsView(APIView):
    permission_classes = [IsAuthenticated]

    # Администраторы (.user.is_staff == True) получают полный список тикетов, остальные - только те тикеты, авторами
    # которых являются.
    def get(self, request):
        if request.user.is_staff:
            tickets = Ticket.objects.all()
        else:
            tickets = Ticket.objects.filter(author_id=request.user.id)
        serializer = TicketsViewSerializer(tickets, many=True)
        return Response({"tickets": serializer.data})

    # При создании нового тикета создаются записи в моделях Ticket и Message. После валидации данных (поле
    # 'text' отдельно проверяем на наличие) производится запись в Ticket, из результата записи берется ее ID и
    # используется в качестве внешнего ключа при записи в Message. Затем отправляются письма юзеру и админу.
    def post(self, request):
        ticket = request.data.get('new_ticket')
        ticket['author'] = str(request.user.id)
        ticket_serializer = TicketSerializer(data=ticket)
        if ticket_serializer.is_valid(raise_exception=True) and ticket.get('text'):
            ticket_saved = ticket_serializer.save()
            ticket['ticket'] = str(ticket_saved.id)
            message_serializer = MessageSerializer(data=ticket)
            if message_serializer.is_valid():
                message_saved = message_serializer.save()
            send_mail_created_ticket.delay(
                user_id=request.user.id,
                ticket_id=ticket_saved.id,
                title=ticket['title_ticket'],
                text=ticket['text'],
                time=message_saved.created
            )
        else:
            content = {"text": ["This field is required."]}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            "success": f'Ticket <{ticket_saved.title_ticket}> created successfully. Ticket ID: {ticket_saved.id}'
        })


class OneTicketView(APIView):
    permission_classes = [IsAuthenticated & PermissionToOneTicketView]

    def get(self, request, ticket_id):
        ticket = get_object_or_404(Ticket.objects.all(), id=ticket_id)
        self.check_object_permissions(request, ticket)
        ticket_serializer = TicketsViewSerializer(ticket)
        return Response({"ticket": ticket_serializer.data})

    def post(self, request, ticket_id):
        ticket = get_object_or_404(Ticket.objects.all(), id=ticket_id)
        self.check_object_permissions(request, ticket)
        message = request.data.get('new_message')
        message['author'] = str(request.user.id)
        message['ticket'] = str(ticket_id)
        serializer = MessageSerializer(data=message)
        if serializer.is_valid(raise_exception=True):
            message_saved = serializer.save()
            send_mail_added_message.delay(
                author_message_id=str(request.user.id),
                author_ticket_id=ticket.author.id,
                ticket_id=ticket_id,
                title=ticket.title_ticket,
                text=message_saved.text,
                time=message_saved.created
            )

        return Response({
            "success": f'Message <{message_saved.text}> added to ticket <{ticket_id}> successfully.'
        })

    def put(self, request, ticket_id):
        ticket = get_object_or_404(Ticket.objects.all(), pk=ticket_id)
        self.check_object_permissions(request, ticket)
        data = request.data.get('ticket')
        serializer = TicketSerializer(instance=ticket, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            ticket_saved = serializer.save()
            send_mail_change_status_ticket.delay(
                user_id=ticket.author.id,
                ticket_id=ticket_id,
                title=ticket.title_ticket,
                status=ticket_saved.status_ticket
            )
        return Response({
            "success": f'Ticket status is set to <{ticket_saved.status_ticket}> successfully'
        })
