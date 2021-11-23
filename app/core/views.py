from rest_framework import status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.serializers import TicketSerializer, MessageSerializer
from core.permissions import PermissionTicketView
from core.tasks import send_mail_created_ticket, send_mail_change_status_ticket, send_mail_added_message
from core.logic import get_user_tickets
from core.models import Ticket, Message


class TicketViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated & PermissionTicketView]

    def list(self, request):
        queryset = get_user_tickets(request.user)
        serializer = TicketSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        ticket = get_object_or_404(Ticket.objects.all(), pk=pk)
        self.check_object_permissions(request, ticket)
        serializer = TicketSerializer(ticket)
        return Response(serializer.data)

    def create(self, request):
        ticket = request.data.get('ticket')
        ticket['author'] = str(request.user.id)
        serializer = TicketSerializer(data=ticket)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        send_mail_created_ticket.delay(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, pk=None):
        ticket = get_object_or_404(Ticket.objects.all(), pk=pk)
        self.check_object_permissions(request, ticket)
        data = request.data.get('ticket')
        serializer = TicketSerializer(instance=ticket, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        send_mail_change_status_ticket.delay(pk)
        return Response(serializer.data)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(ticket=self.kwargs['ticket_pk'])

    def perform_create(self, serializer):
        instance = serializer.save()
        send_mail_added_message.delay(self.request.user.id, instance.id)
