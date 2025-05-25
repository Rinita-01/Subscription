from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('payments/', include("payments.urls")),
    path('users/', include("users.urls")),
    # path('subscriptions/', include("subscriptions.urls")),
]
