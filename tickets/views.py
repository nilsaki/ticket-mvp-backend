from django.core.mail import send_mail
from django.conf import settings
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Ticket
from .serializers import TicketSerializer


class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        role = getattr(user.profile, "role", "USER")

        if role == "ADMIN":
            return Ticket.objects.all().order_by("-created_at")

        if role == "IT":
            return Ticket.objects.filter(request_type="IT").order_by("-created_at")

        if role == "ATOLYE":
            return Ticket.objects.filter(request_type="ATOLYE").order_by("-created_at")

        return Ticket.objects.filter(created_by=user).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=["post"])
    def assign_to_me(self, request, pk=None):
        ticket = self.get_object()
        ticket.assigned_to = request.user
        ticket.status = "IN_PROGRESS"
        ticket.save()
        return Response(TicketSerializer(ticket).data)

    @action(detail=True, methods=["post"])
    def update_status(self, request, pk=None):
        ticket = self.get_object()

        status_value = request.data.get("status")
        solution_note = request.data.get("solution_note", "")

        allowed_statuses = ["OPEN", "IN_PROGRESS", "WAITING", "RESOLVED", "CLOSED"]

        if status_value not in allowed_statuses:
            return Response({"error": "Geçersiz status"}, status=status.HTTP_400_BAD_REQUEST)

        ticket.status = status_value

        if solution_note:
            ticket.solution_note = solution_note

        ticket.save()

        if status_value in ["RESOLVED", "CLOSED"]:
            user_email = ticket.created_by.email
            if user_email:
                send_mail(
                    subject=f"{ticket.ticket_no} numaralı talebiniz tamamlandı",
                    message=f"Merhaba,\n\n{ticket.title} başlıklı talebiniz {status_value} durumuna alınmıştır.\n\nÇözüm notu: {ticket.solution_note or '-'}",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user_email],
                    fail_silently=True,
                )

        return Response(TicketSerializer(ticket).data)