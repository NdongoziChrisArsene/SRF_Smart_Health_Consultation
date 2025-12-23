from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from reports.models import Report
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()


class ReportGenerationTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            username="admin",
            password="admin123"
        )
        self.client.force_authenticate(self.admin)

    def test_generate_appointment_report(self):
        url = reverse("generate-report")
        response = self.client.post(
            url,
            {
                "report_type": "appointments",
                "date_from": "2025-01-01",
                "date_to": "2025-01-31",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertIn("report_id", response.data)
        self.assertEqual(Report.objects.count(), 1)

    def test_generate_report_invalid_dates(self):
        url = reverse("generate-report")
        response = self.client.post(
            url,
            {
                "report_type": "appointments",
                "date_from": "2025-01-xx",
                "date_to": "2025-01-31",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_download_report_pending(self):
        report = Report.objects.create(
            report_type="appointments",
            generated_by=self.admin,
            is_ready=False
        )
        url = reverse("download-report", args=[report.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(response.data["report_status"], "pending")

    def test_download_report_ready_file(self):
        # Mock a simple PDF file
        file_content = b"%PDF-1.4 mock pdf content"
        uploaded_file = SimpleUploadedFile(
            "test_report.pdf",
            file_content,
            content_type="application/pdf"
        )
        report = Report.objects.create(
            report_type="finance",
            generated_by=self.admin,
            is_ready=True,
            file=uploaded_file
        )
        url = reverse("download-report", args=[report.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get("Content-Disposition"), f'attachment; filename="{report.file.name}"')
        self.assertEqual(response.content, file_content)

    def test_status_endpoint_pending(self):
        report = Report.objects.create(
            report_type="finance",
            generated_by=self.admin,
            is_ready=False
        )
        url = reverse("report-status", args=[report.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["report_status"], "pending")
        self.assertEqual(response.data["report_type"], "finance")

    def test_status_endpoint_ready(self):
        report = Report.objects.create(
            report_type="activity",
            generated_by=self.admin,
            is_ready=True,
            file="reports/sample.pdf"
        )
        url = reverse("report-status", args=[report.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["report_status"], "ready")
        self.assertEqual(response.data["report_type"], "activity")

    def test_status_endpoint_error(self):
        report = Report.objects.create(
            report_type="finance",
            generated_by=self.admin,
            is_ready=True,
            file=None
        )
        url = reverse("report-status", args=[report.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["report_status"], "error")






















































# from rest_framework.test import APITestCase
# from django.urls import reverse
# from django.contrib.auth import get_user_model
# from rest_framework import status
# from reports.models import Report
# from django.core.files.base import ContentFile

# User = get_user_model()


# class ReportGenerationTests(APITestCase):
#     def setUp(self):
#         self.admin = User.objects.create_superuser(
#             username="admin",
#             password="admin123"
#         )
#         self.client.force_authenticate(self.admin)

#     # ------------------------
#     # Generate report tests
#     # ------------------------
#     def test_generate_appointment_report(self):
#         url = reverse("generate-report")

#         response = self.client.post(
#             url,
#             {
#                 "report_type": "appointments",
#                 "date_from": "2025-01-01",
#                 "date_to": "2025-01-31",
#             },
#             format="json",
#         )

#         self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
#         self.assertIn("report_id", response.data)
#         self.assertEqual(Report.objects.count(), 1)

#     # ------------------------
#     # Status endpoint tests
#     # ------------------------
#     def test_report_status_pending(self):
#         report = Report.objects.create(
#             report_type="appointments",
#             generated_by=self.admin,
#             is_ready=False
#         )
#         url = reverse("report-status", kwargs={"pk": report.id})
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data["report_status"], "pending")
#         self.assertEqual(response.data["report_id"], report.id)

#     def test_report_status_ready_with_file(self):
#         report = Report.objects.create(
#             report_type="appointments",
#             generated_by=self.admin,
#             is_ready=True
#         )
#         report.file.save("dummy.pdf", ContentFile(b"PDF content"))
#         url = reverse("report-status", kwargs={"pk": report.id})
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data["report_status"], "ready")
#         self.assertEqual(response.data["report_id"], report.id)

#     def test_report_status_ready_but_file_missing(self):
#         report = Report.objects.create(
#             report_type="appointments",
#             generated_by=self.admin,
#             is_ready=True,
#             file=None
#         )
#         url = reverse("report-status", kwargs={"pk": report.id})
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data["report_status"], "error")
#         self.assertEqual(response.data["report_id"], report.id)

#     # ------------------------
#     # Download report tests
#     # ------------------------
#     def test_download_report_not_ready(self):
#         report = Report.objects.create(
#             report_type="appointments",
#             generated_by=self.admin,
#             is_ready=False
#         )
#         url = reverse("download-report", kwargs={"pk": report.id})
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
#         self.assertEqual(response.data["report_status"], "pending")
#         self.assertEqual(response.data["report_id"], report.id)

#     def test_download_report_ready_with_file(self):
#         report = Report.objects.create(
#             report_type="appointments",
#             generated_by=self.admin,
#             is_ready=True
#         )
#         report.file.save("dummy.pdf", ContentFile(b"PDF content"))
#         url = reverse("download-report", kwargs={"pk": report.id})
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         # Response should be a FileResponse
#         self.assertIn("Content-Disposition", response.headers)
#         self.assertTrue(response.headers["Content-Disposition"].startswith("attachment"))
#         self.assertEqual(response.headers["Content-Type"], "application/octet-stream")

#     def test_download_report_ready_file_missing(self):
#         report = Report.objects.create(
#             report_type="appointments",
#             generated_by=self.admin,
#             is_ready=True,
#             file=None
#         )
#         url = reverse("download-report", kwargs={"pk": report.id})
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
#         self.assertEqual(response.data["report_status"], "error")
#         self.assertEqual(response.data["report_id"], report.id)



























































# from rest_framework.test import APITestCase
# from django.urls import reverse
# from django.contrib.auth import get_user_model
# from rest_framework import status
# from reports.models import Report

# User = get_user_model()

# class ReportGenerationTests(APITestCase):
#     def setUp(self):
#         self.admin = User.objects.create_superuser(
#             username="admin",
#             password="admin123"
#         )
#         self.client.force_authenticate(self.admin)

#     def test_generate_appointment_report(self):
#         url = reverse("generate-report")

#         response = self.client.post(
#             url,
#             {
#                 "report_type": "appointments",
#                 "date_from": "2025-01-01",
#                 "date_to": "2025-01-31",
#             },
#             format="json",
#         )

#         self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
#         self.assertIn("report_id", response.data)
#         self.assertEqual(Report.objects.count(), 1)
























# from rest_framework.test import APITestCase
# from django.urls import reverse
# from django.contrib.auth import get_user_model
# from rest_framework import status

# User = get_user_model()

# class ReportGenerationTests(APITestCase):
#     def setUp(self):
#         self.admin = User.objects.create_superuser(
#             username="admin",
#             password="admin123"
#         )
#         self.client.force_authenticate(self.admin)

#     def test_generate_appointment_report(self):
#         response = self.client.post(
#             "/api/reports/generate/",
#             {
#                 "report_type": "appointments",
#                 "date_from": "2025-01-01",
#                 "date_to": "2025-01-31",
#             },
#             format="json"
#         )
#         self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

