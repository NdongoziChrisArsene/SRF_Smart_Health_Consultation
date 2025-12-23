from rest_framework import generics, permissions
from rest_framework.exceptions import NotFound
from .models import PatientProfile
from .serializers import PatientSerializer, UpdatePatientSerializer


class PatientProfileView(generics.RetrieveUpdateAPIView):
    """
    Single endpoint for retrieving and updating the patient's profile.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        try:
            return PatientProfile.objects.get(user=self.request.user)
        except PatientProfile.DoesNotExist:
            raise NotFound("Patient profile not found")

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return UpdatePatientSerializer
        return PatientSerializer








































# from rest_framework import generics, permissions
# from rest_framework.exceptions import NotFound
# from .models import PatientProfile
# from .serializers import PatientSerializer, UpdatePatientSerializer


# class PatientProfileView(generics.RetrieveUpdateAPIView):
#     """
#     Retrieve or update the authenticated patient's profile.
#     """
#     permission_classes = [permissions.IsAuthenticated]

#     def get_object(self):
#         try:
#             return PatientProfile.objects.get(user=self.request.user)
#         except PatientProfile.DoesNotExist:
#             raise NotFound("Patient profile not found")

#     def get_serializer_class(self):
#         if self.request.method in ("PUT", "PATCH"):
#             return UpdatePatientSerializer
#         return PatientSerializer











































# from rest_framework import generics, permissions
# from rest_framework.exceptions import NotFound
# from .models import PatientProfile
# from .serializers import PatientSerializer, UpdatePatientSerializer


# class PatientProfileView(generics.RetrieveUpdateAPIView):
#     """
#     Single endpoint for retrieving and updating the patient's profile.
#     """
#     serializer_class = PatientSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_object(self):
#         try:
#             return PatientProfile.objects.get(user=self.request.user)
#         except PatientProfile.DoesNotExist:
#             raise NotFound("Patient profile not found")

#     def get_serializer_class(self):
#         if self.request.method in ["PUT", "PATCH"]:
#             return UpdatePatientSerializer
#         return PatientSerializer 





































# from rest_framework import generics, permissions
# from rest_framework.exceptions import NotFound
# from .models import PatientProfile
# from .serializers import PatientSerializer, UpdatePatientSerializer


# class PatientProfileView(generics.RetrieveUpdateAPIView):
#     """
#     Retrieve or update the authenticated patient's profile.
#     """
    
#     permission_classes = [permissions.IsAuthenticated]

#     def get_object(self):
#         try:
#             return PatientProfile.objects.get(user=self.request.user)
#         except PatientProfile.DoesNotExist:
#             raise NotFound("Patient profile not found")

#     def get_serializer_class(self):
#         if self.request.method in ("PUT", "PATCH"):
#             return UpdatePatientSerializer
#         return PatientSerializer












































# from rest_framework import generics, permissions
# from rest_framework.exceptions import NotFound
# from .models import PatientProfile
# from .serializers import PatientSerializer, UpdatePatientSerializer


# class PatientProfileView(generics.RetrieveUpdateAPIView):
#     """
#     Single endpoint for retrieving and updating the patient's profile.
#     """
#     serializer_class = PatientSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_object(self):
#         try:
#             return PatientProfile.objects.get(user=self.request.user)
#         except PatientProfile.DoesNotExist:
#             raise NotFound("Patient profile not found")

#     def get_serializer_class(self):
#         if self.request.method in ["PUT", "PATCH"]:
#             return UpdatePatientSerializer
#         return PatientSerializer













































# from rest_framework import generics, permissions
# from rest_framework.exceptions import NotFound
# from .models import Patient
# from .serializers import PatientSerializer, UpdatePatientSerializer


# class PatientProfileView(generics.RetrieveUpdateAPIView):
#     """
#     Single endpoint for retrieving and updating the patient's profile.
#     """
#     serializer_class = PatientSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_object(self):
#         try:
#             return Patient.objects.get(user=self.request.user)
#         except Patient.DoesNotExist:
#             raise NotFound("Patient profile not found")

#     def get_serializer_class(self):
#         if self.request.method in ["PUT", "PATCH"]:
#             return UpdatePatientSerializer
#         return PatientSerializer 

































# from rest_framework import generics, permissions  
# from rest_framework.exceptions import NotFound   
# from .models import Patient             
# from .serializers import PatientSerializer, UpdatePatientSerializer       


# class PatientProfileView(generics.RetrieveUpdateAPIView):
#     serializer_class = PatientSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_object(self):
#         try:
#             return Patient.objects.get(user=self.request.user)
#         except Patient.DoesNotExist:
#             raise NotFound("Patient profile not found")

        
        
# class UpdatePatientProfileView(generics.UpdateAPIView):      
#     serializer_class = UpdatePatientSerializer   
#     permission_classes = [permissions.IsAuthenticated]        
    
    
#     def get_object(self):    
#         try: 
#             return Patient.objects.get(user=self.request.user)    
#         except Patient.DoesNotExist:     
#             raise NotFound("Patient profile not found") 

