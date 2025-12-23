from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import PatientProfile

User = get_user_model()


@receiver(post_save, sender=User)
def create_patient_profile(sender, instance, created, **kwargs):
    """
    Automatically create a PatientProfile for users with role='patient'.
    """
    if created and getattr(instance, "role", None) == "patient":
        PatientProfile.objects.get_or_create(user=instance)








































# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from users.models import User
# from .models import PatientProfile


# @receiver(post_save, sender=User)
# def create_patient_profile(sender, instance, created, **kwargs):
#     """
#     Automatically create a PatientProfile for new users with role 'patient'.
#     """
#     if created and hasattr(instance, "role") and instance.role == "patient":
#         PatientProfile.objects.get_or_create(user=instance)

























# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from users.models import User
# from .models import Patient


# @receiver(post_save, sender=User)
# def create_patient_profile(sender, instance, created, **kwargs):
#     """
#     Automatically create a Patient profile for new users with role 'patient'.
#     """
#     if created and hasattr(instance, "role") and instance.role == "patient":
#         Patient.objects.get_or_create(user=instance)




































# from django.db.models.signals import post_save  
# from django.dispatch import receiver 
# from users.models import User 
# from .models import Patient                   


# @receiver(post_save, sender=User) 
# def create_patient_profile(sender, instance, created, **kwargs): 
#     if created and instance.role == 'patient':
#         Patient.objects.get_or_create(user=instance)
