from django.db import models
from django.conf import settings


class PatientProfile(models.Model):
    GENDER_CHOICES = (
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="patient_profile",
    )

    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        blank=True,
    )
    medical_history = models.TextField(
        blank=True,
        null=True,
        default="",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Patient Profile"
        verbose_name_plural = "Patient Profiles"
        ordering = ["-created_at"]

    def __str__(self):
        return f"PatientProfile(user={self.user.username})"










































# from django.db import models
# from django.conf import settings


# class PatientProfile(models.Model):
#     GENDER_CHOICES = (
#         ("male", "Male"),
#         ("female", "Female"),
#         ("other", "Other"),
#     )

#     user = models.OneToOneField(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name="patient_profile"
#     )

#     age = models.PositiveIntegerField(null=True, blank=True)
#     gender = models.CharField(
#         max_length=10,
#         choices=GENDER_CHOICES,
#         blank=True
#     )
#     medical_history = models.TextField(
#         blank=True,
#         null=True,
#         default=""
#     )

#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         verbose_name = "Patient Profile"
#         verbose_name_plural = "Patient Profiles"
#         ordering = ["-created_at"]

#     def __str__(self):
#         return f"Patient: {self.user.username}"












































# from django.db import models
# from django.conf import settings


# class PatientProfile(models.Model):
#     GENDER_CHOICES = (
#         ("male", "Male"),
#         ("female", "Female"),
#         ("other", "Other"),
#     )

#     user = models.OneToOneField(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name="patient_profile"
#     )

#     age = models.PositiveIntegerField(null=True, blank=True)
#     gender = models.CharField(
#         max_length=10,
#         choices=GENDER_CHOICES,
#         blank=True
#     )
#     medical_history = models.TextField(
#         blank=True,
#         null=True,
#         default=""
#     )

#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         verbose_name = "Patient Profile"
#         verbose_name_plural = "Patient Profiles"
#         ordering = ["-created_at"]

#     def __str__(self):
#         return f"Patient: {self.user.username}"
















































# from django.db import models
# from django.conf import settings


# class PatientProfile(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="patient_profile")

#     age = models.PositiveIntegerField(null=True, blank=True)
#     GENDER_CHOICES = (
#         ("male", "Male"),
#         ("female", "Female"),
#         ("other", "Other"),
#     )
#     gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
#     medical_history = models.TextField(blank=True, null=True, default="")

#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"Patient: {self.user.username}"




























# from django.db import models  
# from django.conf import settings   


# class Patient(models.Model): 
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
#     age = models.PositiveIntegerField(null=True, blank=True)

#     GENDER_CHOICES = (
#         ("male", "Male"),
#         ("female", "Female"),
#         ("other", "Other"),
#     )
#     gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
#     medical_history = models.TextField(blank=True, default="")
     
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     def __str__(self):
#         return f"Patient: {self.user.username}"
