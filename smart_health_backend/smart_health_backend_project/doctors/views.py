from rest_framework import generics, permissions
from rest_framework.exceptions import NotFound
from .models import DoctorProfile, Availability
from .serializers import DoctorSerializer, AvailabilitySerializer
from users.permissions import IsDoctor


class DoctorProfileView(generics.RetrieveUpdateAPIView):
    """
    Retrieve & update the authenticated doctor's profile.
    """
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated, IsDoctor]

    def get_object(self):
        doctor = getattr(self.request.user, "doctor_profile", None)
        if not doctor:
            raise NotFound("Doctor profile not found")
        return doctor


class AvailabilityListCreateView(generics.ListCreateAPIView):
    serializer_class = AvailabilitySerializer
    permission_classes = [permissions.IsAuthenticated, IsDoctor]

    def get_queryset(self):
        doctor = getattr(self.request.user, "doctor_profile", None)
        if not doctor:
            raise NotFound("Doctor profile not found")
        return Availability.objects.filter(doctor=doctor)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["doctor"] = getattr(self.request.user, "doctor_profile", None)
        return context

    def perform_create(self, serializer):
        doctor = getattr(self.request.user, "doctor_profile", None)
        instance = serializer.save(doctor=doctor)
        instance.full_clean()
        instance.save()


class AvailabilityDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AvailabilitySerializer
    permission_classes = [permissions.IsAuthenticated, IsDoctor]

    def get_queryset(self):
        doctor = getattr(self.request.user, "doctor_profile", None)
        if not doctor:
            raise NotFound("Doctor profile not found")
        return Availability.objects.filter(doctor=doctor)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["doctor"] = getattr(self.request.user, "doctor_profile", None)
        return context

































# from rest_framework import generics, permissions
# from rest_framework.exceptions import NotFound
# from .models import DoctorProfile, Availability
# from .serializers import DoctorSerializer, AvailabilitySerializer
# from users.permissions import IsDoctor


# class DoctorProfileView(generics.RetrieveUpdateAPIView):
#     """
#     GET: Retrieve doctor profile
#     PATCH: Update doctor profile
#     """
#     serializer_class = DoctorSerializer
#     permission_classes = [permissions.IsAuthenticated, IsDoctor]

#     def get_object(self):
#         try:
#             return Doctor.objects.get(user=self.request.user)
#         except Doctor.DoesNotExist:
#             raise NotFound("Doctor profile not found")

#     def get_doctor(self):
#         doctor = getattr(self.request.user, "doctor_profile", None)
#         if not doctor:
#             raise NotFound("Doctor profile not found")
#         return doctor



# class AvailabilityListCreateView(generics.ListCreateAPIView):
#     serializer_class = AvailabilitySerializer
#     permission_classes = [permissions.IsAuthenticated, IsDoctor]

#     def get_queryset(self):
#         doctor = getattr(self.request.user, "doctor_profile", None)
#         if not doctor:
#             raise NotFound("Doctor profile not found")

#         return Availability.objects.filter(doctor=doctor)

#     def get_serializer_context(self):
#         context = super().get_serializer_context()
#         context["doctor"] = getattr(self.request.user, "doctor_profile", None)
#         return context

#     def perform_create(self, serializer):
#         doctor = getattr(self.request.user, "doctor_profile", None)
#         instance = serializer.save(doctor=doctor)
#         instance.full_clean()
#         instance.save()


# class AvailabilityDetailView(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = AvailabilitySerializer
#     permission_classes = [permissions.IsAuthenticated, IsDoctor]

#     def get_queryset(self):
#         doctor = getattr(self.request.user, "doctor_profile", None)
#         if not doctor:
#             raise NotFound("Doctor profile not found")

#         return Availability.objects.filter(doctor=doctor)

#     def get_serializer_context(self):
#         context = super().get_serializer_context()
#         context["doctor"] = getattr(self.request.user, "doctor_profile", None)
#         return context
