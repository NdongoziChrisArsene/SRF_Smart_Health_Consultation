from django.db.models.signals import post_save
from django.dispatch import receiver
from django.apps import apps
from users.models import User

@receiver(post_save, sender=User)
def create_profiles(sender, instance, created, **kwargs):
    if not created:
        return

    if instance.role == User.ROLE_PATIENT:
        PatientProfile = apps.get_model("patients", "PatientProfile")
        PatientProfile.objects.get_or_create(user=instance)

    elif instance.role == User.ROLE_DOCTOR:
        DoctorProfile = apps.get_model("doctors", "DoctorProfile")
        DoctorProfile.objects.get_or_create(user=instance)



































# # users/signals.py
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from users.models import User
# from patients.models import PatientProfile
# from doctors.models import DoctorProfile

# @receiver(post_save, sender=User)
# def create_profiles(sender, instance, created, **kwargs):
#     if created and instance.role == "patient":
#         PatientProfile.objects.get_or_create(user=instance)
#     elif created and instance.role == "doctor":
#         DoctorProfile.objects.create(user=instance)
