from django.shortcuts import render
from .models import SubscriptionPlan

def show(request):
    plans = SubscriptionPlan.objects.all()
    return render(request, 'subscriptions/subscriptions.html', {'plans': plans})
