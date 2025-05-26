from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from .models import Payment
from subscriptions.models import SubscriptionPlan
from users.decoraters import custom_login_required
import razorpay

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

@custom_login_required
def payment(request):
    return render(request, 'payments/payment.html')

@custom_login_required
def create_order(request):
    if request.method == 'POST':
        try:
            amount = int(request.POST.get("amount"))
            plan_id = request.POST.get("plan_id")

            if not amount or amount <= 0 or not plan_id:
                return JsonResponse({"error": "Invalid data provided."})

            order_data = {
                "amount": amount,
                "currency": "INR",
                "payment_capture": True
            }

            order_response = client.order.create(order_data)

            if 'id' not in order_response:
                return JsonResponse({"error": "Failed to create Razorpay order."})

            # Create Payment record only
            Payment.objects.create(
                user=request.user,
                amount=amount / 100,  # convert from paise
                payment_method='Razorpay',
                status='Pending',
                is_paid=False,
                transaction_id=order_response['id']
            )

            return JsonResponse({
                "order_id": order_response['id'],
                "key": settings.RAZORPAY_KEY_ID,
                "amount": amount,
                "plan_id": plan_id
            })
        except Exception as e:
            return JsonResponse({"error": str(e)})
    return JsonResponse({"error": "Invalid request"})


@custom_login_required
def verify_payment(request):
    if request.method == "POST":
        try:
            data = request.POST
            razorpay_order_id = data.get("razorpay_order_id")
            razorpay_payment_id = data.get("razorpay_payment_id")
            razorpay_signature = data.get("razorpay_signature")
            plan_id = data.get("plan_id")

            if not all([razorpay_order_id, razorpay_payment_id, razorpay_signature, plan_id]):
                return JsonResponse({"error": "Missing required fields."})

            # Verify Razorpay signature
            client.utility.verify_payment_signature({
                "razorpay_order_id": razorpay_order_id,
                "razorpay_payment_id": razorpay_payment_id,
                "razorpay_signature": razorpay_signature,
            })

            # Update Payment record
            payment = Payment.objects.get(transaction_id=razorpay_order_id)
            payment.status = 'Success'
            payment.is_paid = True
            payment.save()

            # Assign subscription to user
            plan = get_object_or_404(SubscriptionPlan, id=plan_id)

            duration_days = {
                'monthly': 30,
                'quarterly': 90,
                'yearly': 365
            }.get(plan.duration.lower(), 30)

            start_date = datetime.now()
            end_date = start_date + timedelta(days=duration_days)

            Subscription.objects.create(
                user=request.user,
                plan=plan,
                start_date=start_date,
                end_date=end_date,
                is_active=True
            )

            return JsonResponse({
                "success": True,
                "message": "Subscription activated successfully.",
                "plan_id": plan.id
            })

        except razorpay.errors.SignatureVerificationError:
            return JsonResponse({"error": "Payment verification failed (invalid signature)."})

        except Exception as e:
            return JsonResponse({"error": str(e)})

    return JsonResponse({"error": "Invalid request method"})