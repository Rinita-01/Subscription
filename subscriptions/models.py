from django.db import models

class SubscriptionPlan(models.Model):
    DURATION_CHOICES = [
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    duration = models.CharField(max_length=10, choices=DURATION_CHOICES)

    def __str__(self):
        return self.name


class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.end_date and self.plan:
            duration_map = {
                'monthly': 30,
                'quarterly': 90,
                'yearly': 365
            }
            days = duration_map.get(self.plan.duration, 30)
            self.end_date = self.start_date + timedelta(days=days)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.email} - {self.plan.name} ({'Active' if self.is_active else 'Expired'})"
