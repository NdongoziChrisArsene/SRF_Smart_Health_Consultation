from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from datetime import date, timedelta, time
from unittest.mock import patch
from django.utils import timezone

from users.models import User
from patients.models import Patient
from doctors.models import Doctor, Availability
from appointments.models import Appointment
from rest_framework.exceptions import ValidationError


class AppointmentTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create users
        self.patient_user = User.objects.create_user(
            username="pat",
            password="test1234",
            email="p@example.com",
            role="patient"
        )
        self.doctor_user = User.objects.create_user(
            username="doc",
            password="test1234",
            email="d@example.com",
            role="doctor"
        )
        self.admin_user = User.objects.create_superuser(
            username="admin",
            password="admin123",
            email="a@example.com"
        )

        # Create profiles
        self.patient = Patient.objects.create(user=self.patient_user)
        self.doctor = Doctor.objects.create(
            user=self.doctor_user,
            specialization="Cardiology",
            location="City Hospital",
            years_of_experience=5
        )

        # URLs
        self.create_url = reverse("patient-create")
        self.list_url = reverse("patient-list")

    # 1️⃣ Patient creates appointment + double booking check
    @patch("appointments.views.notify_appointment_booked")
    def test_patient_create_and_conflict_prevention(self, mock_notify):
        mock_notify.return_value = True
        self.client.force_authenticate(user=self.patient_user)

        future_date = timezone.now().date() + timedelta(days=2)
        day_of_week = future_date.strftime("%A")

        Availability.objects.create(
            doctor=self.doctor,
            day_of_week=day_of_week,
            start_time=time(9, 0),
            end_time=time(12, 0),
        )

        payload = {
            "doctor": self.doctor.id,
            "date": future_date,
            "time": "10:00",
            "reason_for_visit": "General check-up"
        }

        response = self.client.post(self.create_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        mock_notify.assert_called_once()

        response2 = self.client.post(self.create_url, payload, format="json")
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)

    # 2️⃣ Patient cancels appointment
    @patch("appointments.views.notify_appointment_cancelled")
    def test_patient_cancel(self, mock_notify):
        mock_notify.return_value = True
        self.client.force_authenticate(user=self.patient_user)

        appt = Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            date=date.today() + timedelta(days=3),
            time=time(9, 0),
        )

        cancel_url = reverse("patient-cancel", args=[appt.id])
        response = self.client.patch(cancel_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        appt.refresh_from_db()
        self.assertEqual(appt.status, Appointment.STATUS_CANCELLED)
        mock_notify.assert_called_once()


    # 3️⃣ Doctor lists appointments & updates status
    def test_doctor_list_and_update_status(self):
        self.client.force_authenticate(user=self.doctor_user)

        appt = Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            date=date.today() + timedelta(days=4),
            time=time(8, 0)
        )

        list_url = reverse("doctor-list")
        response = self.client.get(list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any(item["id"] == appt.id for item in response.json()))

        update_url = reverse("doctor-update-status", args=[appt.id])
        response2 = self.client.patch(update_url, {"status": "approved"}, format="json")

        self.assertIn(response2.status_code, [status.HTTP_200_OK, status.HTTP_202_ACCEPTED])

        appt.refresh_from_db()
        self.assertEqual(appt.status, "approved")

    # 4️⃣ Admin lists all appointments
    def test_admin_list_all(self):
        Appointment.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            date=date.today() + timedelta(days=5),
            time=time(11, 0)
        )

        self.client.force_authenticate(user=self.admin_user)

        url = reverse("admin-all")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.json()), 0)


class AppointmentEdgeCaseTests(AppointmentTests): 
    
    @patch("appointments.views.notify_appointment_booked")
    def test_booking_in_past(self, mock_notify):
        mock_notify.return_value = True
        self.client.force_authenticate(user=self.patient_user)
        past_date = timezone.now().date() - timedelta(days=1)
        payload = {
            "doctor": self.doctor.id,
            "date": past_date,
            "time": "10:00",
            "reason_for_visit": "Check-up past"
        }
        response = self.client.post(self.create_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) 
        
        
    @patch("appointments.views.notify_appointment_booked")
    def test_booking_outside_availability(self, mock_notify):
        mock_notify.return_value = True
        self.client.force_authenticate(user=self.patient_user)
        future_date = timezone.now().date() + timedelta(days=2)
        payload = {
            "doctor": self.doctor.id,
            "date": future_date,
            "time": "15:00",  # assuming doctor is available 9-12
            "reason_for_visit": "Outside availability"
        }
        response = self.client.post(self.create_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) 










































# from django.test import TestCase
# from django.urls import reverse
# from rest_framework.test import APIClient
# from rest_framework import status
# from datetime import date, timedelta, time
# from unittest.mock import patch
# from django.utils import timezone

# from users.models import User
# from patients.models import Patient
# from doctors.models import Doctor, Availability
# from appointments.models import Appointment


# class AppointmentTests(TestCase):
#     def setUp(self):
#         self.client = APIClient()

#         # Create users
#         self.patient_user = User.objects.create_user(
#             username="pat",
#             password="test1234",
#             email="p@example.com",
#             role="patient"
#         )
#         self.doctor_user = User.objects.create_user(
#             username="doc",
#             password="test1234",
#             email="d@example.com",
#             role="doctor"
#         )
#         self.admin_user = User.objects.create_superuser(
#             username="admin",
#             password="admin123",
#             email="a@example.com"
#         )

#         # Create profiles
#         self.patient = Patient.objects.create(user=self.patient_user)
#         self.doctor = Doctor.objects.create(
#             user=self.doctor_user,
#             specialization="Cardiology",
#             location="City Hospital",
#             years_of_experience=5
#         )

#         # URLs
#         self.create_url = reverse("patient-create")
#         self.list_url = reverse("patient-list")

#     # 1️⃣ Patient creates appointment + double booking check
#     @patch("appointments.views.notify_appointment_booked")
#     def test_patient_create_and_conflict_prevention(self, mock_notify):
#         mock_notify.return_value = True
#         self.client.force_authenticate(user=self.patient_user)

#         payload = {
#             "doctor": self.doctor.id,
#             "date": date.today() + timedelta(days=2),
#             "time": "10:00",
#             "reason_for_visit": "General check-up"
#         }

#         # First creation succeeds
#         response = self.client.post(self.create_url, payload, format="json")
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         mock_notify.assert_called_once()

#         # Second creation fails (double booking)
#         response2 = self.client.post(self.create_url, payload, format="json")
#         self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)

#     # 2️⃣ Patient cancels appointment
#     @patch("appointments.views.notify_appointment_cancelled")
#     def test_patient_cancel(self, mock_notify):
#         mock_notify.return_value = True
#         self.client.force_authenticate(user=self.patient_user)

#         appt = Appointment.objects.create(
#             patient=self.patient,
#             doctor=self.doctor,
#             date=date.today() + timedelta(days=3), 
#             start_time=time(9, 0),
#             end_time=time(12, 0),
#         )

#         cancel_url = reverse("patient-cancel", args=[appt.id])
#         response = self.client.patch(cancel_url)


#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

#         appt.refresh_from_db()
#         self.assertEqual(appt.status, "cancelled")
#         mock_notify.assert_called_once()

#     # 3️⃣ Doctor lists appointments & updates status
#     def test_doctor_list_and_update_status(self):
#         self.client.force_authenticate(user=self.doctor_user)

#         appt = Appointment.objects.create(
#             patient=self.patient,
#             doctor=self.doctor,
#             date=date.today() + timedelta(days=4),
#             time=time(8, 0)
#         )

#         # List appointments
#         list_url = reverse("doctor-list")
#         response = self.client.get(list_url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertTrue(any(item["id"] == appt.id for item in response.json()))

#         # Update status
#         update_url = reverse("doctor-update-status", args=[appt.id])
#         response2 = self.client.patch(update_url, {"status": "approved"}, format="json")

#         self.assertIn(response2.status_code, [status.HTTP_200_OK, status.HTTP_202_ACCEPTED])

#         appt.refresh_from_db()
#         self.assertEqual(appt.status, "approved")

#     # 4️⃣ Admin lists all appointments
#     def test_admin_list_all(self):
#         Appointment.objects.create(
#             patient=self.patient,
#             doctor=self.doctor,
#             date=date.today() + timedelta(days=5),
#             time=time(11, 0)
#         )

#         self.client.force_authenticate(user=self.admin_user)

#         url = reverse("admin-all")
#         response = self.client.get(url)

#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertGreater(len(response.json()), 0)


    






























