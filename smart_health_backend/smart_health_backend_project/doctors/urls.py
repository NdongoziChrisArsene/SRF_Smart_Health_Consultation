from django.urls import path
from .views import (
    DoctorProfileView,
    AvailabilityListCreateView,
    AvailabilityDetailView,
)

urlpatterns = [
    path("profile/", DoctorProfileView.as_view(), name="doctor-profile"),
    path("availability/", AvailabilityListCreateView.as_view(), name="doctor-availability"),
    path("availability/<int:pk>/", AvailabilityDetailView.as_view(), name="doctor-availability-detail"),
]





























# from django.urls import path    
# from .views import DoctorProfileView, AvailabilityListCreateView, AvailabilityDetailView



# urlpatterns = [
#     path('profile/', DoctorProfileView.as_view(), name="doctor-profile"),    
#     path('availability/', AvailabilityListCreateView.as_view(), name="doctor-availability"),  
#     path('availability/<int:pk>/', AvailabilityDetailView.as_view(), name="doctor-availability-detail"),   
# ]