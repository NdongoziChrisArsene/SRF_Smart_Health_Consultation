from django.urls import path
from .views import (
    PatientCreateAppointmentView,
    PatientAppointmentsView,
    PatientCancelAppointmentView,
    DoctorAppointmentsView,
    DoctorUpdateAppointmentStatusView,
    AdminAllAppointmentsView,
)

urlpatterns = [
    path("patient/create/", PatientCreateAppointmentView.as_view(), name="patient-create"),
    path("patient/list/", PatientAppointmentsView.as_view(), name="patient-list"),
    path("patient/cancel/<int:pk>/", PatientCancelAppointmentView.as_view(), name="patient-cancel"),

    path("doctor/list/", DoctorAppointmentsView.as_view(), name="doctor-list"),
    path("doctor/update-status/<int:pk>/", DoctorUpdateAppointmentStatusView.as_view(), name="doctor-update-status"),

    path("admin/all/", AdminAllAppointmentsView.as_view(), name="admin-all"),
]




































# from django.urls import path
# from .views import (
#     PatientCreateAppointmentView,
#     PatientAppointmentsView,
#     PatientCancelAppointmentView,
#     DoctorAppointmentsView,
#     DoctorUpdateAppointmentStatusView,
#     AdminAllAppointmentsView,
# )

# urlpatterns = [
#     # --------------------------
#     # Patient Routes
#     # --------------------------
#     path(
#         "patient/create/",
#         PatientCreateAppointmentView.as_view(),
#         name="patient-create"
#     ),

#     path(
#         "patient/list/",
#         PatientAppointmentsView.as_view(),
#         name="patient-list"
#     ),

#     path(
#         "patient/cancel/<int:pk>/",
#         PatientCancelAppointmentView.as_view(),
#         name="patient-cancel"
#     ),

#     # --------------------------
#     # Doctor Routes
#     # --------------------------
#     path(
#         "doctor/list/",
#         DoctorAppointmentsView.as_view(),
#         name="doctor-list"
#     ),

#     path(
#         "doctor/update-status/<int:pk>/",
#         DoctorUpdateAppointmentStatusView.as_view(),
#         name="doctor-update-status"
#     ),

#     # --------------------------
#     # Admin Routes
#     # --------------------------
#     path(
#         "admin/all/",
#         AdminAllAppointmentsView.as_view(),
#         name="admin-all"
#     ),
# ]









































# from django.urls import path
# from .views import (
#     PatientCreateAppointmentView,
#     PatientAppointmentsView,
#     PatientCancelAppointmentView,
#     DoctorAppointmentsView,
#     DoctorUpdateAppointmentStatusView,
#     AdminAllAppointmentsView,
# )

# urlpatterns = [
#     path("patient/create/", PatientCreateAppointmentView.as_view(), name="patient-create"),
#     path("patient/list/", PatientAppointmentsView.as_view(), name="patient-list"),
#     path("patient/cancel/<int:pk>/", PatientCancelAppointmentView.as_view(), name="patient-cancel"),

#     path("doctor/list/", DoctorAppointmentsView.as_view(), name="doctor-list"),
#     path("doctor/update-status/<int:pk>/", DoctorUpdateAppointmentStatusView.as_view(), name="doctor-update-status"),

#     path("admin/all/", AdminAllAppointmentsView.as_view(), name="admin-all"),
# ]





























































