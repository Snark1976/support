from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter

from core.views import TicketViewSet, MessageViewSet


router = DefaultRouter()
router.register(r'ticket', TicketViewSet, basename='ticket')

ticket_router = NestedSimpleRouter(router, r'ticket', lookup='ticket')
ticket_router.register(r'message', MessageViewSet, basename='ticket-messages')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(ticket_router.urls)),
]
