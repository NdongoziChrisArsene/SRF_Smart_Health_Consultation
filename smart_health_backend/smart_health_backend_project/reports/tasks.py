from celery import shared_task
from django.core.mail import EmailMessage
from django.core.exceptions import ObjectDoesNotExist
from .models import Report
from .services.analytics_service import AnalyticsService
from .services.report_generator import ReportGenerator
import logging

logger = logging.getLogger(__name__)


@shared_task(bind=True, autoretry_for=(Exception,), retry_kwargs={"max_retries": 3})
def generate_report_task(self, report_id, report_type, start_date, end_date, email):
    try:
        report = Report.objects.get(id=report_id)
    except ObjectDoesNotExist:
        logger.error(f"Report with ID {report_id} does not exist.")
        return

    service_map = {
        "appointments": (
            AnalyticsService.appointment_stats,
            "reporting/report_summary.html",
        ),
        "finance": (
            AnalyticsService.financial_stats,
            "reporting/financial_report.html",
        ),
        "activity": (
            AnalyticsService.user_activity_stats,
            "reporting/user_activity_report.html",
        ),
    }

    if report_type not in service_map:
        logger.error(f"Invalid report_type '{report_type}' for Report ID {report_id}.")
        return

    analytics_func, template = service_map[report_type]

    try:
        data = analytics_func(start_date, end_date)
    except Exception as e:
        logger.error(f"Analytics calculation failed for report {report_id}: {e}")
        return

    try:
        pdf_file = ReportGenerator.generate_pdf(
            template=template,
            context={**data, "start_date": start_date, "end_date": end_date},
        )
        pdf_file.name = f"{report_type}_report.pdf"
        report.file.save(pdf_file.name, pdf_file)
        report.is_ready = True
        report.save()
    except Exception as e:
        logger.error(f"Failed to generate or save PDF for report {report_id}: {e}")
        return

    # Send email safely
    if email:
        try:
            email_msg = EmailMessage(
                subject="Your Report Is Ready",
                body="Please find your generated report attached.",
                to=[email],
            )
            if report.file:
                email_msg.attach_file(report.file.path)
            email_msg.send()
        except Exception as e:
            logger.warning(f"Failed to send report email for report {report_id} to {email}: {e}")
    else:
        logger.warning(f"No email provided for report {report_id}. Skipping email sending.")








































# from celery import shared_task
# from django.core.mail import EmailMessage
# from .models import Report
# from .services.analytics_service import AnalyticsService
# from .services.report_generator import ReportGenerator


# @shared_task(bind=True, autoretry_for=(Exception,), retry_kwargs={"max_retries": 3})
# def generate_report_task(self, report_id, report_type, start_date, end_date, email):
#     report = Report.objects.get(id=report_id)

#     service_map = {
#         "appointments": (
#             AnalyticsService.appointment_stats,
#             "reporting/report_summary.html",
#         ),
#         "finance": (
#             AnalyticsService.financial_stats,
#             "reporting/financial_report.html",
#         ),
#         "activity": (
#             AnalyticsService.user_activity_stats,
#             "reporting/user_activity_report.html",
#         ),
#     }

#     analytics_func, template = service_map[report_type]
#     data = analytics_func(start_date, end_date)

#     pdf_file = ReportGenerator.generate_pdf(
#         template=template,
#         context={**data, "start_date": start_date, "end_date": end_date},
#     )
#     pdf_file.name = f"{report_type}_report.pdf"

#     report.file.save(pdf_file.name, pdf_file)
#     report.is_ready = True
#     report.save()

#     # 📧 Email report (SAFE)
#     email_msg = EmailMessage(
#         subject="Your Report Is Ready",
#         body="Please find your generated report attached.",
#         to=[email],
#     )
#     email_msg.attach_file(report.file.path)
#     email_msg.send()
























































# from celery import shared_task
# from django.core.mail import EmailMessage
# from django.core.files.base import ContentFile
# from .models import Report
# from .services.analytics_service import AnalyticsService
# from .services.report_generator import ReportGenerator


# @shared_task(bind=True, autoretry_for=(Exception,), retry_kwargs={"max_retries": 3})
# def generate_report_task(self, report_id, report_type, start_date, end_date, email):
#     report = Report.objects.get(id=report_id)

#     service_map = {
#         "appointments": (AnalyticsService.appointment_stats, "reporting/report_summary.html"),
#         "finance": (AnalyticsService.financial_stats, "reporting/financial_report.html"),
#         "activity": (AnalyticsService.user_activity_stats, "reporting/user_activity_report.html"),
#     }

#     analytics_func, template = service_map[report_type]
#     data = analytics_func(start_date, end_date)

#     pdf_file = ReportGenerator.generate_pdf(
#         template=template,
#         context={**data, "start_date": start_date, "end_date": end_date},
#     )
#     pdf_file.name = f"{report_type}_report.pdf"

#     report.file.save(pdf_file.name, pdf_file)
#     report.is_ready = True
#     report.save()

#     # 📧 Email report
#     email_msg = EmailMessage(
#         subject="Your Report Is Ready",
#         body="Please find your generated report attached.",
#         to=[email],
#     )
#     email_msg.attach(pdf_file.name, pdf_file.read(), "application/pdf")
#     email_msg.send()
