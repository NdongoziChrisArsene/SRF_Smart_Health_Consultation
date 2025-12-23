from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import User
from .models import DoctorProfile


@receiver(post_save, sender=User)
def create_doctor_profile(sender, instance, created, **kwargs):
    """
    Auto-create DoctorProfile when a doctor user is created.
    """
    if created and getattr(instance, "role", None) == "doctor":
        DoctorProfile.objects.get_or_create(user=instance)



























# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from users.models import User
# from .models import DoctorProfile


# @receiver(post_save, sender=User)
# def create_doctor_profile(sender, instance, created, **kwargs):
#     """
#     Automatically creates a Doctor profile ONLY when:
#     - A new User is created
#     - User.role == 'doctor'
#     """
#     if created and getattr(instance, "role", None) == "doctor":
#         DoctorProfile.objects.get_or_create(user=instance)
