from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime

from patients.models import PatientProfile
from doctors.models import DoctorProfile, Availability


class Appointment(models.Model):
    STATUS_PENDING = "pending"
    STATUS_APPROVED = "approved"
    STATUS_CANCELLED = "cancelled"
    STATUS_COMPLETED = "completed"

    STATUS_CHOICES = (
        (STATUS_PENDING, "Pending"),
        (STATUS_APPROVED, "Approved"),
        (STATUS_CANCELLED, "Cancelled"),
        (STATUS_COMPLETED, "Completed"),
    )

    patient = models.ForeignKey(
        PatientProfile,
        on_delete=models.CASCADE,
        related_name="appointments"
    )
    doctor = models.ForeignKey(
        DoctorProfile,
        on_delete=models.CASCADE,
        related_name="appointments"
    )

    # Optional but linked availability
    availability = models.ForeignKey(
        Availability,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="appointments"
    )

    date = models.DateField()
    time = models.TimeField()
    reason_for_visit = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        unique_together = (
            ("doctor", "date", "time"),
            ("patient", "date", "time"),
        )
        indexes = [
            models.Index(fields=["doctor", "date", "time"]),
            models.Index(fields=["patient", "date", "time"]),
        ]

    def __str__(self):
        return (
            f"{self.patient.user.username} → "
            f"{self.doctor.user.username} on {self.date} at {self.time}"
        )

    def clean(self):
        appointment_dt = datetime.combine(self.date, self.time)
        if timezone.is_naive(appointment_dt):
            appointment_dt = timezone.make_aware(appointment_dt)

        if appointment_dt < timezone.now() and self.status != self.STATUS_COMPLETED:
            raise ValidationError("Cannot schedule an appointment in the past.")

        if Appointment.objects.filter(
            doctor=self.doctor,
            date=self.date,
            time=self.time
        ).exclude(pk=self.pk).exists():
            raise ValidationError("Doctor already has an appointment at this time.")

        if Appointment.objects.filter(
            patient=self.patient,
            date=self.date,
            time=self.time
        ).exclude(pk=self.pk).exists():
            raise ValidationError("You already have an appointment at this time.")

        if self.availability:
            if self.availability.doctor != self.doctor:
                raise ValidationError("Availability does not belong to this doctor.")

            if self.availability.day_of_week != self.date.strftime("%A"):
                raise ValidationError("Availability does not match appointment date.")

            if not (
                self.availability.start_time <= self.time < self.availability.end_time
            ):
                raise ValidationError("Time is outside availability window.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)








































# from django.db import models
# from django.core.exceptions import ValidationError
# from django.utils import timezone
# from datetime import datetime


# class Appointment(models.Model):
#     STATUS_PENDING = "pending"
#     STATUS_APPROVED = "approved"
#     STATUS_CANCELLED = "cancelled"
#     STATUS_COMPLETED = "completed"

#     STATUS_CHOICES = (
#         (STATUS_PENDING, "Pending"),
#         (STATUS_APPROVED, "Approved"),
#         (STATUS_CANCELLED, "Cancelled"),
#         (STATUS_COMPLETED, "Completed"),
#     )

#     patient = models.ForeignKey(
#         "patients.PatientProfile",
#         on_delete=models.CASCADE,
#         related_name="appointments"
#     )

#     doctor = models.ForeignKey(
#         "doctors.DoctorProfile",
#         on_delete=models.CASCADE,
#         related_name="appointments"
#     )

#     date = models.DateField()
#     time = models.TimeField()
#     reason_for_visit = models.TextField(blank=True)
#     status = models.CharField(
#         max_length=20,
#         choices=STATUS_CHOICES,
#         default=STATUS_PENDING
#     )

#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         ordering = ["-created_at"]
#         unique_together = (
#             ("doctor", "date", "time"),
#             ("patient", "date", "time"),
#         )
#         indexes = [
#             models.Index(fields=["doctor", "date", "time"]),
#             models.Index(fields=["patient", "date", "time"]),
#         ]

#     def __str__(self):
#         return f"{self.patient.user.username} → {self.doctor.user.username} on {self.date} at {self.time}"

#     def clean(self):
#         appointment_dt = datetime.combine(self.date, self.time)
#         if timezone.is_naive(appointment_dt):
#             appointment_dt = timezone.make_aware(appointment_dt)

#         if appointment_dt < timezone.now() and self.status != self.STATUS_COMPLETED:
#             raise ValidationError("Cannot schedule an appointment in the past.")

#         if Appointment.objects.filter(
#             doctor=self.doctor,
#             date=self.date,
#             time=self.time
#         ).exclude(pk=self.pk).exists():
#             raise ValidationError("This doctor already has an appointment at this time.")

#         if Appointment.objects.filter(
#             patient=self.patient,
#             date=self.date,
#             time=self.time
#         ).exclude(pk=self.pk).exists():
#             raise ValidationError("You already have an appointment at this time.")

#     def save(self, *args, **kwargs):
#         self.full_clean()
#         super().save(*args, **kwargs)




































































# from django.db import models
# from django.core.exceptions import ValidationError
# from django.utils import timezone
# from datetime import datetime
# from patients.models import PatientProfile
# from doctors.models import DoctorProfile


# class Appointment(models.Model):
#     STATUS_PENDING = "pending"
#     STATUS_APPROVED = "approved"
#     STATUS_CANCELLED = "cancelled"
#     STATUS_COMPLETED = "completed"

#     STATUS_CHOICES = (
#         (STATUS_PENDING, "Pending"),
#         (STATUS_APPROVED, "Approved"),
#         (STATUS_CANCELLED, "Cancelled"),
#         (STATUS_COMPLETED, "Completed"),
#     )

#     patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name="appointments")
#     doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name="appointments")

#     date = models.DateField()
#     time = models.TimeField()
#     reason_for_visit = models.TextField(blank=True)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)

#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         ordering = ["-created_at"]
#         unique_together = (
#             ("doctor", "date", "time"),
#             ("patient", "date", "time"),
#         )
#         indexes = [
#             models.Index(fields=["doctor", "date", "time"]),
#             models.Index(fields=["patient", "date", "time"]),
#         ]

#     def __str__(self):
#         return f"{self.patient.user.username} → {self.doctor.user.username} on {self.date} at {self.time}"

#     def clean(self):
#         appointment_dt = datetime.combine(self.date, self.time)
#         if timezone.is_naive(appointment_dt):
#             appointment_dt = timezone.make_aware(appointment_dt)

#         if appointment_dt < timezone.now() and self.status != self.STATUS_COMPLETED:
#             raise ValidationError("Cannot schedule an appointment in the past.")

#         if Appointment.objects.filter(
#             doctor=self.doctor, date=self.date, time=self.time
#         ).exclude(pk=self.pk).exists():
#             raise ValidationError("This doctor already has an appointment at this time.")

#         if Appointment.objects.filter(
#             patient=self.patient, date=self.date, time=self.time
#         ).exclude(pk=self.pk).exists():
#             raise ValidationError("You already have an appointment at this time.")

#     def save(self, *args, **kwargs):
#         self.full_clean()
#         super().save(*args, **kwargs)





































# from django.db import models
# from django.core.exceptions import ValidationError
# from django.utils import timezone
# from datetime import datetime 
# from patients.models import Patient
# from doctors.models import Doctor


# class Appointment(models.Model):
#     STATUS_PENDING = "pending"
#     STATUS_APPROVED = "approved"
#     STATUS_CANCELLED = "cancelled"
#     STATUS_COMPLETED = "completed"

#     STATUS_CHOICES = (
#         (STATUS_PENDING, "Pending"),
#         (STATUS_APPROVED, "Approved"),
#         (STATUS_CANCELLED, "Cancelled"),
#         (STATUS_COMPLETED, "Completed"),
#     )

#     patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="appointments")
#     doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="appointments")

#     date = models.DateField()
#     time = models.TimeField()
#     reason_for_visit = models.TextField(blank=True)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)

#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         ordering = ["-created_at"]
#         unique_together = (
#             ("doctor", "date", "time"),
#             ("patient", "date", "time"),
#         )

#     def __str__(self):
#         return f"{self.patient.user.username} → {self.doctor.user.username} on {self.date} at {self.time}"

#     def clean(self):
#         appointment_dt = datetime.combine(self.date, self.time)
#         if timezone.is_naive(appointment_dt): 
#             appointment_dt = timezone.make_aware(appointment_dt)    

#         if appointment_dt < timezone.now() and self.status != self.STATUS_COMPLETED:
#             raise ValidationError("Cannot schedule an appointment in the past.")

#         if Appointment.objects.filter(doctor=self.doctor, date=self.date, time=self.time).exclude(pk=self.pk).exists():
#             raise ValidationError("This doctor already has an appointment at this time.")

#         if Appointment.objects.filter(patient=self.patient, date=self.date, time=self.time).exclude(pk=self.pk).exists():
#             raise ValidationError("You already have an appointment at this time.")

#     def save(self, *args, **kwargs):
#         self.full_clean()
#         super().save(*args, **kwargs)





















