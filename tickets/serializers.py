from rest_framework import serializers
from .models import Ticket, UserProfile


class TicketSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source="created_by.username", read_only=True)
    assigned_to_name = serializers.CharField(source="assigned_to.username", read_only=True)

    class Meta:
        model = Ticket
        fields = [
            "id",
            "ticket_no",
            "created_by",
            "created_by_name",
            "assigned_to",
            "assigned_to_name",
            "request_type",
            "category",
            "title",
            "description",
            "priority",
            "status",
            "solution_note",
            "created_at",
            "updated_at",
            "resolved_at",
            "closed_at",
        ]
        read_only_fields = ["id", "ticket_no", "created_by", "created_at", "updated_at"]


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = UserProfile
        fields = ["id", "username", "role", "department"]