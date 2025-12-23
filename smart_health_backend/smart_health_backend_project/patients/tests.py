from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import PatientProfile

User = get_user_model()


class PatientProfileTests(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username="patient1",
            email="patient1@example.com",
            password="securepassword",
            role="patient",
        )

        # Ensure a PatientProfile exists
        self.profile = PatientProfile.objects.create(user=self.user)

        # Authenticate the client
        self.client.force_authenticate(user=self.user)

        # URL for profile endpoint
        self.url = reverse("patient-profile")

    def test_retrieve_patient_profile(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], self.user.username)
        self.assertEqual(response.data["email"], self.user.email)

    def test_partial_update_profile(self):
        response = self.client.patch(self.url, {"age": 30})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        profile = PatientProfile.objects.get(user=self.user)
        self.assertEqual(profile.age, 30)

    def test_full_update_profile(self):
        payload = {
            "age": 35,
            "gender": "female",
            "medical_history": "Diabetic",
        }
        response = self.client.put(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        profile = PatientProfile.objects.get(user=self.user)
        self.assertEqual(profile.age, 35)
        self.assertEqual(profile.gender, "female")
        self.assertEqual(profile.medical_history, "Diabetic")

    def test_profile_not_found(self):
        # Delete the profile
        PatientProfile.objects.filter(user=self.user).delete()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)











































# from django.urls import reverse
# from rest_framework import status
# from rest_framework.test import APITestCase
# from django.contrib.auth import get_user_model
# from .models import PatientProfile

# User = get_user_model()


# class PatientProfileTests(APITestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(
#             username="patient1",
#             email="patient1@example.com",
#             password="securepassword",
#             role="patient",
#         )
#         self.profile = PatientProfile.objects.create(user=self.user)
#         self.client.force_authenticate(self.user)
#         self.url = reverse("patient-profile")

#     def test_retrieve_patient_profile(self):
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data["username"], self.user.username)

#     def test_partial_update_profile(self):
#         response = self.client.patch(self.url, {"age": 30})
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#         profile = PatientProfile.objects.get(user=self.user)
#         self.assertEqual(profile.age, 30)

#     def test_full_update_profile(self):
#         payload = {
#             "age": 35,
#             "gender": "female",
#             "medical_history": "Diabetic",
#         }
#         response = self.client.put(self.url, payload)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#         profile = PatientProfile.objects.get(user=self.user)
#         self.assertEqual(profile.gender, "female")

#     def test_profile_not_found(self):
#         PatientProfile.objects.filter(user=self.user).delete()
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

































# from django.urls import reverse
# from rest_framework import status
# from rest_framework.test import APITestCase
# from django.contrib.auth import get_user_model
# from .models import PatientProfile

# User = get_user_model()


# class PatientProfileTests(APITestCase):
#     def setUp(self):
#         # Create a patient user
#         self.user = User.objects.create_user(
#             username="patient1",
#             email="patient1@example.com",
#             password="securepassword",
#             role="patient"
#         )
#         # Signal auto-creates PatientProfile
#         self.patient = PatientProfile.objects.get(user=self.user)
#         self.client.force_authenticate(user=self.user)
#         self.url = reverse("patient-profile")

#     def test_retrieve_patient_profile(self):
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data["username"], self.user.username)
#         self.assertEqual(response.data["email"], self.user.email)

#     def test_update_patient_profile_partial(self):
#         payload = {"age": 30, "medical_history": "No allergies"}
#         response = self.client.patch(self.url, data=payload)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.patient.refresh_from_db()
#         self.assertEqual(self.patient.age, 30)
#         self.assertEqual(self.patient.medical_history, "No allergies")

#     def test_update_patient_profile_full(self):
#         payload = {"age": 35, "gender": "female", "medical_history": "Diabetic"}
#         response = self.client.put(self.url, data=payload)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.patient.refresh_from_db()
#         self.assertEqual(self.patient.age, 35)
#         self.assertEqual(self.patient.gender, "female")
#         self.assertEqual(self.patient.medical_history, "Diabetic")

#     def test_patient_profile_not_found(self):
#         self.patient.delete()
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#         self.assertEqual(response.data["detail"], "Patient profile not found")


















































# from django.urls import reverse
# from rest_framework import status
# from rest_framework.test import APITestCase
# from django.contrib.auth import get_user_model
# from .models import Patient

# User = get_user_model()

# class PatientProfileTests(APITestCase):
#     def setUp(self):
#         # Create a patient user
#         self.user = User.objects.create_user(
#             username="patient1",
#             email="patient1@example.com",
#             password="securepassword",
#             role="patient"
#         )
#         # Signal should auto-create Patient profile
#         self.patient = Patient.objects.get(user=self.user)
#         self.client.force_authenticate(user=self.user)
#         self.url = reverse("patient-profile")

#     def test_retrieve_patient_profile(self):
#         """Test retrieving the patient profile"""
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data["username"], self.user.username)
#         self.assertEqual(response.data["email"], self.user.email)

#     def test_update_patient_profile_partial(self):
#         """Test partially updating the patient profile"""
#         payload = {"age": 30, "medical_history": "No allergies"}
#         response = self.client.patch(self.url, data=payload)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.patient.refresh_from_db()
#         self.assertEqual(self.patient.age, 30)
#         self.assertEqual(self.patient.medical_history, "No allergies")

#     def test_update_patient_profile_full(self):
#         """Test fully updating the patient profile"""
#         payload = {"age": 35, "gender": "female", "medical_history": "Diabetic"}
#         response = self.client.put(self.url, data=payload)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.patient.refresh_from_db()
#         self.assertEqual(self.patient.age, 35)
#         self.assertEqual(self.patient.gender, "female")
#         self.assertEqual(self.patient.medical_history, "Diabetic")

#     def test_update_patient_profile_medical_history_null(self):
#         """Ensure medical_history can be null or empty"""
#         payload = {"medical_history": ""}
#         response = self.client.patch(self.url, data=payload)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.patient.refresh_from_db()
#         self.assertEqual(self.patient.medical_history, "")

#         payload_null = {"medical_history": None}
#         response = self.client.patch(self.url, data=payload_null)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.patient.refresh_from_db()
#         self.assertIsNone(self.patient.medical_history)

#     def test_patient_profile_not_found(self):
#         """Test behavior when patient profile does not exist"""
#         # Delete the patient instance
#         self.patient.delete()
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#         self.assertEqual(response.data["detail"], "Patient profile not found")

#     def test_unauthenticated_access(self):
#         """Ensure unauthenticated users cannot access profile"""
#         self.client.force_authenticate(user=None)
#         response = self.client.get(self.url)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
