from django.contrib import admin
from .models import Report


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ("id", "report_type", "generated_by", "is_ready", "created_at")
    list_filter = ("report_type", "is_ready")
    search_fields = ("generated_by__username",)
    readonly_fields = ("created_at",)
