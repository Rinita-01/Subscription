from django.urls import path
from . import views

urlpatterns = [
    path("payment/", views.payment, name="payment"),
    path("create_order/", views.create_order, name="create_order"),
    path("verify_payment/", views.verify_payment, name="verify_payment"),
    path("success/<int:subscription_id>/", views.success, name='success'),
]
