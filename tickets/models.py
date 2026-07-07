from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ("USER", "User"),
        ("IT", "IT"),
        ("ATOLYE", "Atölye"),
        ("ADMIN", "Admin"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="USER")
    department = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"


class Ticket(models.Model):
    REQUEST_TYPE_CHOICES = [
        ("IT", "IT"),
        ("ATOLYE", "Atölye"),
    ]

    PRIORITY_CHOICES = [
        ("LOW", "Düşük"),
        ("MEDIUM", "Orta"),
        ("HIGH", "Yüksek"),
        ("CRITICAL", "Kritik"),
    ]

    STATUS_CHOICES = [
        ("OPEN", "Açık"),
        ("IN_PROGRESS", "İşlemde"),
        ("WAITING", "Beklemede"),
        ("RESOLVED", "Çözüldü"),
        ("CLOSED", "Kapandı"),
    ]

    ticket_no = models.CharField(max_length=30, unique=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_tickets")
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_tickets")

    request_type = models.CharField(max_length=20, choices=REQUEST_TYPE_CHOICES)
    category = models.CharField(max_length=100, blank=True, null=True)

    title = models.CharField(max_length=200)
    description = models.TextField()

    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default="MEDIUM")
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="OPEN")

    solution_note = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(blank=True, null=True)
    closed_at = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.ticket_no:
            last_id = Ticket.objects.count() + 1
            self.ticket_no = f"TCK-{last_id:05d}"

        if self.status == "RESOLVED" and not self.resolved_at:
            self.resolved_at = timezone.now()

        if self.status == "CLOSED" and not self.closed_at:
            self.closed_at = timezone.now()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.ticket_no} - {self.title}"