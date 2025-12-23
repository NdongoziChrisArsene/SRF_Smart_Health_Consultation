from django.db import models
from django.conf import settings


class Report(models.Model):
    REPORT_TYPES = (
        ("appointments", "Appointments"),
        ("finance", "Finance"),
        ("activity", "User Activity"),
    )

    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    generated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reports"
    )
    file = models.FileField(upload_to="reports/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_ready = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.report_type} - {self.created_at.date()}"

































# from django.db import models
# from django.conf import settings

# class Report(models.Model):
#     REPORT_TYPES = (
#         ("appointments", "Appointments"),
#         ("finance", "Finance"),
#         ("activity", "Activity"),
#     )

#     report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
#     generated_by = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name="generated_reports"
#     )
#     file = models.FileField(upload_to="reports/")
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.report_type} report ({self.created_at.date()})"
































# from django.db import models
# from django.contrib.auth import get_user_model
# from django.core.exceptions import ValidationError

# User = get_user_model()


# class Report(models.Model):
#     REPORT_TYPES = (
#         ("appointments", "Appointments Report"),
#         ("finance", "Financial Report"),
#         ("activity", "User Activity Report"),
#     )

#     title = models.CharField(max_length=255)
#     report_type = models.CharField(max_length=50, choices=REPORT_TYPES)
#     generated_by = models.ForeignKey(
#         User,
#         on_delete=models.SET_NULL,
#         null=True,
#         related_name="generated_reports"
#     )

#     date_from = models.DateField()
#     date_to = models.DateField()

#     file = models.FileField(upload_to="reports/", null=True, blank=True)

#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ["-created_at"]
#         verbose_name = "Report"
#         verbose_name_plural = "Reports"
#         # Optional safety against duplicates
#         unique_together = ("report_type", "date_from", "date_to")

#     def __str__(self):
#         return f"{self.title} ({self.get_report_type_display()})"

#     def clean(self):
#         """Ensure date range is valid before saving."""
#         if self.date_from and self.date_to and self.date_from > self.date_to:
#             raise ValidationError("date_from cannot be later than date_to")

#     @property
#     def report_period(self):
#         """Human-readable date range."""
#         return f"{self.date_from} → {self.date_to}"

#     def filename(self):
#         """Return the stored file name cleanly."""
#         return self.file.name.split("/")[-1] if self.file else None


















































# from django.db import models
# from django.contrib.auth import get_user_model

# User = get_user_model()

# class Report(models.Model):
#     REPORT_TYPES = (
#         ("appointments", "Appointments Report"),
#         ("finance", "Financial Report"),
#         ("activity", "User Activity Report"),
#     )

#     title = models.CharField(max_length=255)
#     report_type = models.CharField(max_length=50, choices=REPORT_TYPES)
#     generated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
#     date_from = models.DateField()
#     date_to = models.DateField()

#     created_at = models.DateTimeField(auto_now_add=True)
#     file = models.FileField(upload_to="reports/", null=True, blank=True)

#     def __str__(self):
#         return f"{self.title} ({self.report_type})"
