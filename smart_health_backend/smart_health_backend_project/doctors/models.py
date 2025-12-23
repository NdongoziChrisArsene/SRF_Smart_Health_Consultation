from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


class DoctorProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="doctor_profile"
    )
    specialization = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    years_of_experience = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Doctor: {self.user.username} ({self.specialization})"


class Availability(models.Model):
    DAYS = (
        ("Monday", "Monday"),
        ("Tuesday", "Tuesday"),
        ("Wednesday", "Wednesday"),
        ("Thursday", "Thursday"),
        ("Friday", "Friday"),
        ("Saturday", "Saturday"),
        ("Sunday", "Sunday"),
    )

    doctor = models.ForeignKey(
        DoctorProfile,
        on_delete=models.CASCADE,
        related_name="availabilities"
    )
    day_of_week = models.CharField(max_length=10, choices=DAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        ordering = ["day_of_week", "start_time"]
        unique_together = ("doctor", "day_of_week", "start_time", "end_time")

    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError("Start time must be earlier than end time.")

        overlapping = Availability.objects.filter(
            doctor=self.doctor,
            day_of_week=self.day_of_week,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time,
        ).exclude(id=self.id)

        if overlapping.exists():
            raise ValidationError("This time overlaps with another availability.")

    def __str__(self):
        return f"{self.doctor.user.username} - {self.day_of_week} ({self.start_time}-{self.end_time})"







































# from django.db import models
# from django.conf import settings
# from django.core.exceptions import ValidationError


# class DoctorProfile(models.Model):
#     user = models.OneToOneField(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name="doctor_profile"
#     )
#     specialization = models.CharField(max_length=100)
#     location = models.CharField(max_length=100)
#     years_of_experience = models.PositiveIntegerField(default=0)

#     def __str__(self):
#         return f"Doctor: {self.user.username} ({self.specialization})"


# class Availability(models.Model):
#     DAYS = (
#         ("Monday", "Monday"),
#         ("Tuesday", "Tuesday"),
#         ("Wednesday", "Wednesday"),
#         ("Thursday", "Thursday"),
#         ("Friday", "Friday"),
#         ("Saturday", "Saturday"),
#         ("Sunday", "Sunday"),
#     )

#     doctor = models.ForeignKey(
#         "doctors.DoctorProfile",   # ✅ FIXED HERE
#         on_delete=models.CASCADE,
#         related_name="availabilities"
#     )
#     day_of_week = models.CharField(max_length=10, choices=DAYS)
#     start_time = models.TimeField()
#     end_time = models.TimeField()

#     class Meta:
#         ordering = ["day_of_week", "start_time"]
#         unique_together = ("doctor", "day_of_week", "start_time", "end_time")

#     def clean(self):
#         if self.start_time >= self.end_time:
#             raise ValidationError("Start time must be earlier than end time.")

#         overlapping = Availability.objects.filter(
#             doctor=self.doctor,
#             day_of_week=self.day_of_week,
#             start_time__lt=self.end_time,
#             end_time__gt=self.start_time,
#         ).exclude(id=self.id)

#         if overlapping.exists():
#             raise ValidationError("This time overlaps with another availability.")

#     def __str__(self):
#         return (
#             f"{self.doctor.user.username} - "
#             f"{self.day_of_week}: {self.start_time}-{self.end_time}"
#         )













































# from django.db import models
# from django.conf import settings
# from django.core.exceptions import ValidationError


# class DoctorProfile(models.Model):
#     user = models.OneToOneField(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name="doctor_profile"
#     )
#     specialization = models.CharField(max_length=100)
#     location = models.CharField(max_length=100)
#     years_of_experience = models.PositiveIntegerField(default=0)

#     def __str__(self):
#         return f"Doctor: {self.user.username} ({self.specialization})"


# class Availability(models.Model):
#     DAYS = (
#         ("Monday", "Monday"),
#         ("Tuesday", "Tuesday"),
#         ("Wednesday", "Wednesday"),
#         ("Thursday", "Thursday"),
#         ("Friday", "Friday"),
#         ("Saturday", "Saturday"),
#         ("Sunday", "Sunday"),
#     )

#     doctor = models.ForeignKey(
#         Doctor,
#         on_delete=models.CASCADE,
#         related_name="availabilities"
#     )
#     day_of_week = models.CharField(max_length=10, choices=DAYS)
#     start_time = models.TimeField()
#     end_time = models.TimeField()

#     class Meta:
#         ordering = ["day_of_week", "start_time"]
#         unique_together = ("doctor", "day_of_week", "start_time", "end_time")

#     def clean(self):
#         # Basic validation
#         if self.start_time >= self.end_time:
#             raise ValidationError("Start time must be earlier than end time.")

#         # Overlapping validation
#         overlapping = Availability.objects.filter(
#             doctor=self.doctor,
#             day_of_week=self.day_of_week,
#             start_time__lt=self.end_time,
#             end_time__gt=self.start_time,
#         ).exclude(id=self.id)

#         if overlapping.exists():
#             raise ValidationError(
#                 "This time overlaps with another availability."
#             )

#     def __str__(self):
#         return f"{self.doctor.user.username} - {self.day_of_week}: {self.start_time}-{self.end_time}"
