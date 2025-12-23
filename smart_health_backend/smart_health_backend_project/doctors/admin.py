from django.contrib import admin
from .models import DoctorProfile, Availability


@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "specialization", "location", "years_of_experience")
    search_fields = ("user__username", "specialization")


@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ("doctor", "day_of_week", "start_time", "end_time")
    list_filter = ("day_of_week",)
