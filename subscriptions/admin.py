from django.contrib import admin
from django.utils.html import format_html
from .models import SubscriptionPlan

@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration', 'image_preview')
    search_fields = ('name',)
    list_filter = ('duration',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="60" height="60" style="object-fit:cover;"/>', obj.image.url)
        return "-"
    image_preview.short_description = "Image"
