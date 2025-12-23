from rest_framework import generics, permissions, filters, status
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from users.permissions import IsPatient, IsDoctor
from .models import Appointment
from .serializers import (
    AppointmentSerializer,
    CreateAppointmentSerializer,
    UpdateAppointmentStatusSerializer,
)
from .utils import (
    notify_appointment_booked,
    notify_appointment_cancelled,
)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class PatientCreateAppointmentView(generics.CreateAPIView):
    serializer_class = CreateAppointmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsPatient]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    def perform_create(self, serializer):
        patient = getattr(self.request.user, "patient_profile", None)
        if not patient:
            raise NotFound("Patient profile not found.")

        appointment = serializer.save(patient=patient)
        notify_appointment_booked(
            patient=appointment.patient,
            doctor=appointment.doctor,
            appointment=appointment
        )


class PatientAppointmentsView(generics.ListAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsPatient]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["doctor__user__username", "reason_for_visit"]
    ordering_fields = ["date", "created_at"]

    def get_queryset(self):
        patient = getattr(self.request.user, "patient_profile", None)
        if not patient:
            raise NotFound("Patient profile not found.")
        return Appointment.objects.filter(patient=patient)


class PatientCancelAppointmentView(generics.UpdateAPIView):
    serializer_class = UpdateAppointmentStatusSerializer
    permission_classes = [permissions.IsAuthenticated, IsPatient]

    def get_queryset(self):
        patient = getattr(self.request.user, "patient_profile", None)
        if not patient:
            raise NotFound("Patient profile not found.")
        return Appointment.objects.filter(patient=patient)

    def patch(self, request, *args, **kwargs):
        appointment = self.get_object()
        serializer = self.get_serializer(
            appointment,
            data={"status": Appointment.STATUS_CANCELLED},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        notify_appointment_cancelled(
            patient=appointment.patient,
            appointment=appointment
        )
        return Response(status=status.HTTP_204_NO_CONTENT)


class DoctorAppointmentsView(generics.ListAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsDoctor]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        doctor = getattr(self.request.user, "doctor_profile", None)
        if not doctor:
            raise NotFound("Doctor profile not found.")
        return Appointment.objects.filter(doctor=doctor)


class DoctorUpdateAppointmentStatusView(generics.UpdateAPIView):
    serializer_class = UpdateAppointmentStatusSerializer
    permission_classes = [permissions.IsAuthenticated, IsDoctor]

    def get_queryset(self):
        doctor = getattr(self.request.user, "doctor_profile", None)
        if not doctor:
            raise NotFound("Doctor profile not found.")
        return Appointment.objects.filter(doctor=doctor)


class AdminAllAppointmentsView(generics.ListAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAdminUser]
    pagination_class = StandardResultsSetPagination
    queryset = Appointment.objects.all()

















































# from rest_framework import generics, permissions, filters, status
# from rest_framework.exceptions import NotFound
# from rest_framework.pagination import PageNumberPagination
# from rest_framework.response import Response
# from .models import Appointment
# from .serializers import (
#     AppointmentSerializer,
#     CreateAppointmentSerializer,
#     UpdateAppointmentStatusSerializer,
# )
# from users.permissions import IsPatient, IsDoctor
# from .utils import notify_appointment_booked, notify_appointment_cancelled


# class StandardResultsSetPagination(PageNumberPagination):
#     page_size = 10
#     page_size_query_param = "page_size"
#     max_page_size = 100


# class PatientCreateAppointmentView(generics.CreateAPIView):
#     serializer_class = CreateAppointmentSerializer
#     permission_classes = [permissions.IsAuthenticated, IsPatient]

#     def get_serializer_context(self):
#         ctx = super().get_serializer_context()
#         ctx["request"] = self.request
#         return ctx

#     def perform_create(self, serializer):
#         patient = getattr(self.request.user, "patient_profile", None)
#         if not patient:
#             raise NotFound("Patient profile not found.")

#         appointment = serializer.save(patient=patient)
#         notify_appointment_booked(patient=appointment.patient, doctor=appointment.doctor, appointment=appointment)


# class PatientAppointmentsView(generics.ListAPIView):
#     serializer_class = AppointmentSerializer
#     permission_classes = [permissions.IsAuthenticated, IsPatient]
#     pagination_class = StandardResultsSetPagination
#     filter_backends = [filters.SearchFilter, filters.OrderingFilter]
#     search_fields = ["doctor__user__username", "reason_for_visit"]
#     ordering_fields = ["date", "created_at"]

#     def get_queryset(self):
#         patient = getattr(self.request.user, "patient_profile", None)
#         if not patient:
#             raise NotFound("Patient profile not found.")
#         return Appointment.objects.filter(patient=patient).order_by("-created_at")


# class PatientCancelAppointmentView(generics.UpdateAPIView):
#     """
#     Allows a patient to cancel their appointment.
#     Uses UpdateAppointmentStatusSerializer for consistency with doctor updates.
#     Returns 204 No Content on success.
#     """
#     serializer_class = UpdateAppointmentStatusSerializer
#     permission_classes = [permissions.IsAuthenticated, IsPatient]

#     def get_queryset(self):
#         patient = getattr(self.request.user, "patient_profile", None)
#         if not patient:
#             raise NotFound("Patient profile not found.")
#         return Appointment.objects.filter(patient=patient)

#     def patch(self, request, *args, **kwargs):
#         appointment = self.get_object()
#         # Only allow cancelling
#         serializer = self.get_serializer(
#             appointment, data={"status": Appointment.STATUS_CANCELLED}, partial=True
#         )
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         notify_appointment_cancelled(patient=appointment.patient, appointment=appointment)
#         # Return 204 No Content to match REST conventions
#         return Response(status=status.HTTP_204_NO_CONTENT)



# class DoctorAppointmentsView(generics.ListAPIView):
#     serializer_class = AppointmentSerializer
#     permission_classes = [permissions.IsAuthenticated, IsDoctor]
#     pagination_class = StandardResultsSetPagination
#     filter_backends = [filters.SearchFilter, filters.OrderingFilter]
#     search_fields = ["patient__user__username", "reason_for_visit"]
#     ordering_fields = ["date", "created_at"]

#     def get_queryset(self):
#         doctor = getattr(self.request.user, "doctor_profile", None)
#         if not doctor:
#             raise NotFound("Doctor profile not found.")
#         return Appointment.objects.filter(doctor=doctor).order_by("-created_at")


# class DoctorUpdateAppointmentStatusView(generics.UpdateAPIView):
#     serializer_class = UpdateAppointmentStatusSerializer
#     permission_classes = [permissions.IsAuthenticated, IsDoctor]

#     def get_queryset(self):
#         doctor = getattr(self.request.user, "doctor_profile", None)
#         if not doctor:
#             raise NotFound("Doctor profile not found.")
#         return Appointment.objects.filter(doctor=doctor)

#     def patch(self, request, *args, **kwargs):
#         return self.partial_update(request, *args, **kwargs)


# class AdminAllAppointmentsView(generics.ListAPIView):
#     serializer_class = AppointmentSerializer
#     permission_classes = [permissions.IsAdminUser]
#     pagination_class = StandardResultsSetPagination
#     queryset = Appointment.objects.all().order_by("-created_at")




































# from rest_framework import generics, permissions, filters
# from rest_framework.exceptions import NotFound
# from rest_framework.pagination import PageNumberPagination
# from rest_framework.response import Response
# from rest_framework import status


# from .models import Appointment
# from .serializers import (
#     AppointmentSerializer,
#     CreateAppointmentSerializer,
#     UpdateAppointmentStatusSerializer,
# ) 
# # from .permissions import IsPatient, IsDoctor 
# from users.permissions import IsPatient, IsDoctor
# from .utils import notify_appointment_booked, notify_appointment_cancelled


# # -----------------------------
# # Pagination
# # -----------------------------
# class StandardResultsSetPagination(PageNumberPagination):
#     page_size = 10
#     page_size_query_param = "page_size"
#     max_page_size = 100


# # -----------------------------
# # Patient Views
# # -----------------------------
# class PatientCreateAppointmentView(generics.CreateAPIView):
#     serializer_class = CreateAppointmentSerializer
#     permission_classes = [permissions.IsAuthenticated, IsPatient]

#     def get_serializer_context(self):
#         ctx = super().get_serializer_context()
#         ctx["request"] = self.request
#         return ctx

#     def perform_create(self, serializer):
#         patient = getattr(self.request.user, "patient_profile", None)
#         if not patient:
#             raise NotFound("Patient profile not found.")

#         appointment = serializer.save(patient=patient)

#         # Notify safely
#         notify_appointment_booked(
#             patient=appointment.patient,
#             doctor=appointment.doctor,
#             appointment=appointment
#         )


# class PatientAppointmentsView(generics.ListAPIView):
#     serializer_class = AppointmentSerializer
#     permission_classes = [permissions.IsAuthenticated, IsPatient]
#     pagination_class = StandardResultsSetPagination
#     filter_backends = [filters.SearchFilter, filters.OrderingFilter]
#     search_fields = ["doctor__user__username", "reason_for_visit"]
#     ordering_fields = ["date", "created_at"]

#     def get_queryset(self):
#         patient = getattr(self.request.user, "patient_profile", None)
#         if not patient:
#             raise NotFound("Patient profile not found.")
#         return Appointment.objects.filter(patient=patient).order_by("-created_at")


# class PatientCancelAppointmentView(generics.UpdateAPIView):
#     serializer_class = AppointmentSerializer
#     permission_classes = [permissions.IsAuthenticated, IsPatient]

#     def get_queryset(self):
#         patient = getattr(self.request.user, "patient_profile", None)
#         if not patient:
#             raise NotFound("Patient profile not found.")
#         return Appointment.objects.filter(patient=patient)


#     def patch(self, request, *args, **kwargs):
#         appointment = self.get_object()

#         if appointment.status == "cancelled":
#             return Response(
#                 {"detail": "Appointment already cancelled."},
#                 status=status.HTTP_400_BAD_REQUEST
#             )


#         appointment.status = "cancelled"
#         appointment.save()

#         notify_appointment_cancelled(
#             patient=appointment.patient,
#             appointment=appointment
#         )

#         return Response(status=status.HTTP_204_NO_CONTENT)




# # -----------------------------
# # Doctor Views
# # -----------------------------
# class DoctorAppointmentsView(generics.ListAPIView):
#     serializer_class = AppointmentSerializer
#     permission_classes = [permissions.IsAuthenticated, IsDoctor]
#     pagination_class = StandardResultsSetPagination
#     filter_backends = [filters.SearchFilter, filters.OrderingFilter]
#     search_fields = ["patient__user__username", "reason_for_visit"]
#     ordering_fields = ["date", "created_at"]

#     def get_queryset(self):
#         doctor = getattr(self.request.user, "doctor_profile", None)
#         if not doctor:
#             raise NotFound("Doctor profile not found.")
#         return Appointment.objects.filter(doctor=doctor).order_by("-created_at")


# class DoctorUpdateAppointmentStatusView(generics.UpdateAPIView):
#     serializer_class = UpdateAppointmentStatusSerializer
#     permission_classes = [permissions.IsAuthenticated, IsDoctor]

#     def get_queryset(self):
#         doctor = getattr(self.request.user, "doctor_profile", None)
#         if not doctor:
#             raise NotFound("Doctor profile not found.")
#         return Appointment.objects.filter(doctor=doctor)

#     def patch(self, request, *args, **kwargs):
#         """Allow PATCH requests"""
#         return self.partial_update(request, *args, **kwargs)


# # -----------------------------
# # Admin Views
# # -----------------------------
# class AdminAllAppointmentsView(generics.ListAPIView):
#     serializer_class = AppointmentSerializer
#     permission_classes = [permissions.IsAdminUser]
#     pagination_class = StandardResultsSetPagination
#     queryset = Appointment.objects.all().order_by("-created_at")



























