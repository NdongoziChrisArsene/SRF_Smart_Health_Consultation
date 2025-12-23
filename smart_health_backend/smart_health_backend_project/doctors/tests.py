from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from doctors.models import DoctorProfile, Availability

User = get_user_model()


class DoctorProfileTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="doctor1",
            password="password123",
            role="doctor"
        )
        self.client.force_authenticate(self.user)

    def test_get_doctor_profile(self):
        response = self.client.get(reverse("doctor-profile"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "doctor1")


class AvailabilityTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="doctor2",
            password="password123",
            role="doctor"
        )
        self.client.force_authenticate(self.user)

    def test_create_availability(self):
        payload = {
            "day_of_week": "Monday",
            "start_time": "09:00",
            "end_time": "12:00",
        }
        response = self.client.post(
            reverse("doctor-availability"), payload
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Availability.objects.count(), 1)
