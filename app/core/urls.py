from django.urls import path
from .views import TicketsView, OneTicketView

urlpatterns = [
    path('tickets/', TicketsView.as_view()),
    path('tickets/<int:ticket_id>/', OneTicketView.as_view()),
]
