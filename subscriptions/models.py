from django.db import models
from users.models import User
from django.conf import settings
from django.utils import timezone
from datetime import timedelta


class SubscriptionPlan(models.Model):
    DURATION_CHOICES = [
        ('1M', '1 Month'),
        ('3M', '3 Months'),
        ('6M', '6 Months'),
        ('12M', '12 Months'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    duration = models.CharField(max_length=4, choices=DURATION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)  # ✅ This fixes the error

    def __str__(self):
        return f"{self.name} ({self.get_duration_display()})"



class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.end_date and self.plan:
            duration_map = {
                '1M': 30,
                '3M': 90,
                '6M': 180,
                '12M': 365
            }
            days = duration_map.get(self.plan.duration, 30)
            self.end_date = self.start_date + timedelta(days=days)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.email} - {self.plan.name} ({'Active' if self.is_active else 'Expired'})"
