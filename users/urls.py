from django.urls import path
from .views import ( customer_registration, admin_registration, customer_login, myAccount, logout, activate)

urlpatterns = [
    path('register/', customer_registration, name='customer_registration'),
    path('customer_login/', customer_login, name='customer_login'),
    path('myAccount/', myAccount, name='myAccount'),
    path('logout/', logout, name='logout'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('admin_registration/', admin_registration, name='admin_registration'),
]