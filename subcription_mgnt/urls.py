from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('payments/', include("payments.urls")),
    path('users/', include("users.urls")),
    path('subscription/', include("subscriptions.urls")),
    path('', views.home, name='home'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)