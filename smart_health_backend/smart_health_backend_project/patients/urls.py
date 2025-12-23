from django.urls import path
from .views import PatientProfileView

urlpatterns = [
    path("profile/", PatientProfileView.as_view(), name="patient-profile"),
]
























# from django.urls import path
# from .views import PatientProfileView

# urlpatterns = [
#     path("profile/", PatientProfileView.as_view(), name="patient-profile"),
# ]











# from django.urls import path           
# from .views import PatientProfileView, UpdatePatientProfileView

# urlpatterns = [
#     path('profile/', PatientProfileView.as_view(), name='patient-profile'),
#     path('profile/update/', UpdatePatientProfileView.as_view(), name='update-patient-profile'),
# ] 
