from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    ROLE_PATIENT = "patient"
    ROLE_DOCTOR = "doctor"
    ROLE_ADMIN = "admin"

    ROLE_CHOICES = (
        (ROLE_PATIENT, "Patient"),
        (ROLE_DOCTOR, "Doctor"),
        (ROLE_ADMIN, "Admin"),
    )

    email = models.EmailField(_("email address"), unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_PATIENT)
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255, blank=True)

    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return f"{self.username} ({self.role})"
