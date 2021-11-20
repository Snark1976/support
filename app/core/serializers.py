from rest_framework import serializers
from .models import Ticket, Message


class MessageViewSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username', max_length=150)

    class Meta:
        model = Message
        fields = ['author', 'text', 'created']


class TicketsViewSerializer(serializers.ModelSerializer):
    messages = MessageViewSerializer(many=True)
    author = serializers.CharField(source='author.username', max_length=150)
    status_ticket = serializers.CharField(source='get_status_ticket_display')

    class Meta:
        model = Ticket
        fields = ['id', 'author', 'title_ticket', 'status_ticket', 'messages']


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = '__all__'


class TicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = '__all__'
