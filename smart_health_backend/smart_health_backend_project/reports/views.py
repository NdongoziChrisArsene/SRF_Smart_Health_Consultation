from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.http import FileResponse
from datetime import datetime
import logging

from .models import Report
from .serializers import ReportSerializer
from .permissions import IsAdminUserForReports
from .tasks import generate_report_task

logger = logging.getLogger(__name__)


class GenerateReportView(generics.CreateAPIView):
    serializer_class = ReportSerializer
    permission_classes = [IsAdminUserForReports]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        report_type = request.data.get("report_type")
        start = request.data.get("date_from")
        end = request.data.get("date_to")

        if not start or not end:
            raise ValidationError({"detail": "date_from and date_to are required"})

        if report_type not in dict(Report.REPORT_TYPES):
            raise ValidationError({"detail": "Invalid report_type"})

        try:
            start_date = datetime.strptime(start, "%Y-%m-%d").date()
            end_date = datetime.strptime(end, "%Y-%m-%d").date()
        except ValueError:
            raise ValidationError({"detail": "Invalid date format. Use YYYY-MM-DD."})

        report = serializer.save(generated_by=request.user)

        try:
            # Trigger Celery task asynchronously
            generate_report_task.delay(
                report.id,
                report_type,
                start_date,
                end_date,
                request.user.email,
            )
            task_status = "started"
        except Exception as e:
            logger.error(f"Failed to queue report generation task: {e}")
            task_status = "failed"

        return Response(
            {
                "detail": f"Report generation {task_status}",
                "report_id": report.id,
                "report_status": "pending" if task_status == "started" else "error"
            },
            status=status.HTTP_202_ACCEPTED if task_status == "started" else status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


class DownloadReportView(generics.RetrieveAPIView):
    queryset = Report.objects.all()
    permission_classes = [IsAdminUserForReports]

    def get(self, request, *args, **kwargs):
        report = self.get_object()

        if not report.is_ready:
            return Response(
                {
                    "detail": "Report is not ready yet.",
                    "report_id": report.id,
                    "report_status": "pending"
                },
                status=status.HTTP_202_ACCEPTED
            )

        if not report.file:
            logger.warning(f"Report {report.id} is ready but file is missing.")
            return Response(
                {
                    "detail": "Report file is missing or failed to generate.",
                    "report_id": report.id,
                    "report_status": "error"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # Use 'with' to safely open file
        with report.file.open("rb") as f:
            response = FileResponse(
                f,
                as_attachment=True,
                filename=report.file.name,
            )
        return response



class ReportStatusView(generics.RetrieveAPIView):
    """
    Returns the status of a report without sending the file.
    """
    queryset = Report.objects.all()
    permission_classes = [IsAdminUserForReports]

    def get(self, request, *args, **kwargs):
        report = self.get_object()

        if report.is_ready and report.file:
            report_status = "ready"
        elif report.is_ready and not report.file:
            report_status = "error"
        else:
            report_status = "pending"

        return Response(
            {
                "report_id": report.id,
                "report_type": report.report_type,
                "report_status": report_status,
                "generated_by": report.generated_by.username,
                "created_at": report.created_at,
            },
            status=status.HTTP_200_OK,
        )








































# from rest_framework import generics, status
# from rest_framework.response import Response
# from rest_framework.exceptions import ValidationError
# from django.http import FileResponse
# from datetime import datetime
# import logging

# from .models import Report
# from .serializers import ReportSerializer
# from .permissions import IsAdminUserForReports
# from .tasks import generate_report_task

# logger = logging.getLogger(__name__)


# class GenerateReportView(generics.CreateAPIView):
#     serializer_class = ReportSerializer
#     permission_classes = [IsAdminUserForReports]

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         report_type = request.data.get("report_type")
#         start = request.data.get("date_from")
#         end = request.data.get("date_to")

#         if not start or not end:
#             raise ValidationError({"detail": "date_from and date_to are required"})

#         if report_type not in dict(Report.REPORT_TYPES):
#             raise ValidationError({"detail": "Invalid report_type"})

#         try:
#             start_date = datetime.strptime(start, "%Y-%m-%d").date()
#             end_date = datetime.strptime(end, "%Y-%m-%d").date()
#         except ValueError:
#             raise ValidationError({"detail": "Invalid date format. Use YYYY-MM-DD."})

#         report = serializer.save(generated_by=request.user)

#         try:
#             # Trigger Celery task asynchronously
#             generate_report_task.delay(
#                 report.id,
#                 report_type,
#                 start_date,
#                 end_date,
#                 request.user.email,
#             )
#             task_status = "started"
#         except Exception as e:
#             logger.error(f"Failed to queue report generation task: {e}")
#             task_status = "failed"

#         return Response(
#             {
#                 "detail": f"Report generation {task_status}",
#                 "report_id": report.id,
#                 "report_status": "pending" if task_status == "started" else "error"
#             },
#             status=status.HTTP_202_ACCEPTED if task_status == "started" else status.HTTP_500_INTERNAL_SERVER_ERROR,
#         )


# class DownloadReportView(generics.RetrieveAPIView):
#     queryset = Report.objects.all()
#     permission_classes = [IsAdminUserForReports]

#     def get(self, request, *args, **kwargs):
#         report = self.get_object()

#         if not report.is_ready:
#             return Response(
#                 {
#                     "detail": "Report is not ready yet.",
#                     "report_id": report.id,
#                     "report_status": "pending"
#                 },
#                 status=status.HTTP_202_ACCEPTED
#             )

#         if not report.file:
#             logger.warning(f"Report {report.id} is ready but file is missing.")
#             return Response(
#                 {
#                     "detail": "Report file is missing or failed to generate.",
#                     "report_id": report.id,
#                     "report_status": "error"
#                 },
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )

#         # Use 'with' to safely open file
#         with report.file.open("rb") as f:
#             response = FileResponse(
#                 f,
#                 as_attachment=True,
#                 filename=report.file.name,
#             )
#         return response


# class ReportStatusView(generics.RetrieveAPIView):
#     """
#     Endpoint to check the status of a report without downloading the file.
#     Useful for long-running reports.
#     """
#     queryset = Report.objects.all()
#     permission_classes = [IsAdminUserForReports]

#     def get(self, request, *args, **kwargs):
#         report = self.get_object()

#         if not report.is_ready:
#             report_status = "pending"
#         elif report.is_ready and report.file:
#             report_status = "ready"
#         else:
#             report_status = "error"

#         return Response(
#             {
#                 "report_id": report.id,
#                 "report_status": report_status,
#                 "report_type": report.report_type,
#                 "created_at": report.created_at,
#             },
#             status=status.HTTP_200_OK
#         )












































# from rest_framework import generics, status
# from rest_framework.response import Response
# from rest_framework.exceptions import ValidationError
# from django.http import FileResponse
# from datetime import datetime
# import logging

# from .models import Report
# from .serializers import ReportSerializer
# from .permissions import IsAdminUserForReports
# from .tasks import generate_report_task

# logger = logging.getLogger(__name__)


# class GenerateReportView(generics.CreateAPIView):
#     serializer_class = ReportSerializer
#     permission_classes = [IsAdminUserForReports]

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         report_type = request.data.get("report_type")
#         start = request.data.get("date_from")
#         end = request.data.get("date_to")

#         if not start or not end:
#             raise ValidationError({"detail": "date_from and date_to are required"})

#         if report_type not in dict(Report.REPORT_TYPES):
#             raise ValidationError({"detail": "Invalid report_type"})

#         try:
#             start_date = datetime.strptime(start, "%Y-%m-%d").date()
#             end_date = datetime.strptime(end, "%Y-%m-%d").date()
#         except ValueError:
#             raise ValidationError({"detail": "Invalid date format. Use YYYY-MM-DD."})

#         report = serializer.save(generated_by=request.user)

#         try:
#             # Trigger Celery task asynchronously
#             generate_report_task.delay(
#                 report.id,
#                 report_type,
#                 start_date,
#                 end_date,
#                 request.user.email,
#             )
#             task_status = "started"
#         except Exception as e:
#             logger.error(f"Failed to queue report generation task: {e}")
#             task_status = "failed"

#         return Response(
#             {
#                 "detail": f"Report generation {task_status}",
#                 "report_id": report.id,
#                 "report_status": "pending" if task_status == "started" else "error"
#             },
#             status=status.HTTP_202_ACCEPTED if task_status == "started" else status.HTTP_500_INTERNAL_SERVER_ERROR,
#         )


# class DownloadReportView(generics.RetrieveAPIView):
#     queryset = Report.objects.all()
#     permission_classes = [IsAdminUserForReports]

#     def get(self, request, *args, **kwargs):
#         report = self.get_object()

#         if not report.is_ready:
#             return Response(
#                 {
#                     "detail": "Report is not ready yet.",
#                     "report_id": report.id,
#                     "report_status": "pending"
#                 },
#                 status=status.HTTP_202_ACCEPTED
#             )

#         if not report.file:
#             logger.warning(f"Report {report.id} is ready but file is missing.")
#             return Response(
#                 {
#                     "detail": "Report file is missing or failed to generate.",
#                     "report_id": report.id,
#                     "report_status": "error"
#                 },
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )

#         # Use 'with' to safely open file
#         with report.file.open("rb") as f:
#             response = FileResponse(
#                 f,
#                 as_attachment=True,
#                 filename=report.file.name,
#             )
#         return response


# class ReportStatusView(generics.RetrieveAPIView):
#     """
#     Returns the status of a report: pending, ready, or error.
#     """
#     queryset = Report.objects.all()
#     permission_classes = [IsAdminUserForReports]

#     def get(self, request, *args, **kwargs):
#         report = self.get_object()

#         if report.is_ready and report.file:
#             status_text = "ready"
#         elif report.is_ready and not report.file:
#             status_text = "error"
#         else:
#             status_text = "pending"

#         return Response(
#             {
#                 "report_id": report.id,
#                 "report_type": report.report_type,
#                 "report_status": status_text,
#                 "generated_by": report.generated_by.username,
#                 "created_at": report.created_at,
#             },
#             status=status.HTTP_200_OK
#         )

















































# from rest_framework import generics, status
# from rest_framework.response import Response
# from rest_framework.exceptions import ValidationError
# from django.http import FileResponse
# from datetime import datetime
# import logging

# from .models import Report
# from .serializers import ReportSerializer
# from .permissions import IsAdminUserForReports
# from .tasks import generate_report_task

# logger = logging.getLogger(__name__)


# class GenerateReportView(generics.CreateAPIView):
#     serializer_class = ReportSerializer
#     permission_classes = [IsAdminUserForReports]

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         report_type = request.data.get("report_type")
#         start = request.data.get("date_from")
#         end = request.data.get("date_to")

#         if not start or not end:
#             raise ValidationError({"detail": "date_from and date_to are required"})

#         if report_type not in dict(Report.REPORT_TYPES):
#             raise ValidationError({"detail": "Invalid report_type"})

#         try:
#             start_date = datetime.strptime(start, "%Y-%m-%d").date()
#             end_date = datetime.strptime(end, "%Y-%m-%d").date()
#         except ValueError:
#             raise ValidationError({"detail": "Invalid date format. Use YYYY-MM-DD."})

#         report = serializer.save(generated_by=request.user)

#         try:
#             # Trigger Celery task asynchronously
#             generate_report_task.delay(
#                 report.id,
#                 report_type,
#                 start_date,
#                 end_date,
#                 request.user.email,
#             )
#             task_status = "started"
#         except Exception as e:
#             logger.error(f"Failed to queue report generation task: {e}")
#             task_status = "failed"
        
#         return Response(
#             {
#                 "detail": f"Report generation {task_status}",
#                 "report_id": report.id,
#                 "report_status": "pending" if task_status == "started" else "error"
#             },
#             status=status.HTTP_202_ACCEPTED if task_status == "started" else status.HTTP_500_INTERNAL_SERVER_ERROR,
#         )


# class DownloadReportView(generics.RetrieveAPIView):
#     queryset = Report.objects.all()
#     permission_classes = [IsAdminUserForReports]

#     def get(self, request, *args, **kwargs):
#         report = self.get_object()

#         if not report.is_ready:
#             return Response(
#                 {
#                     "detail": "Report is not ready yet.",
#                     "report_id": report.id,
#                     "report_status": "pending"
#                 },
#                 status=status.HTTP_202_ACCEPTED
#             )

#         if not report.file:
#             logger.warning(f"Report {report.id} is ready but file is missing.")
#             return Response(
#                 {
#                     "detail": "Report file is missing or failed to generate.",
#                     "report_id": report.id,
#                     "report_status": "error"
#                 },
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )

#         # Use 'with' to safely open file
#         with report.file.open("rb") as f:
#             response = FileResponse(
#                 f,
#                 as_attachment=True,
#                 filename=report.file.name,
#             )
#         return response

















































# from rest_framework import generics, status
# from rest_framework.response import Response
# from rest_framework.exceptions import ValidationError
# from django.http import FileResponse
# from datetime import datetime

# from .models import Report
# from .serializers import ReportSerializer
# from .permissions import IsAdminUserForReports
# from .tasks import generate_report_task


# class GenerateReportView(generics.CreateAPIView):
#     serializer_class = ReportSerializer
#     permission_classes = [IsAdminUserForReports]

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         report_type = request.data.get("report_type")
#         start = request.data.get("date_from")
#         end = request.data.get("date_to")

#         if not start or not end:
#             raise ValidationError({"detail": "date_from and date_to are required"})

#         if report_type not in dict(Report.REPORT_TYPES):
#             raise ValidationError({"detail": "Invalid report_type"})

#         try:
#             start_date = datetime.strptime(start, "%Y-%m-%d").date()
#             end_date = datetime.strptime(end, "%Y-%m-%d").date()
#         except ValueError:
#             raise ValidationError({"detail": "Invalid date format. Use YYYY-MM-DD."})

#         report = serializer.save(generated_by=request.user)

#         # Trigger Celery task asynchronously
#         generate_report_task.delay(
#             report.id,
#             report_type,
#             start_date,
#             end_date,
#             request.user.email,
#         )

#         return Response(
#             {"detail": "Report generation started", "report_id": report.id},
#             status=status.HTTP_202_ACCEPTED,
#         )


# class DownloadReportView(generics.RetrieveAPIView):
#     queryset = Report.objects.all()
#     permission_classes = [IsAdminUserForReports]

#     def get(self, request, *args, **kwargs):
#         report = self.get_object()

#         if not report.is_ready:
#             raise ValidationError({"detail": "Report is not ready yet."})

#         # Use 'with' to safely open file
#         with report.file.open("rb") as f:
#             response = FileResponse(
#                 f,
#                 as_attachment=True,
#                 filename=report.file.name,
#             )
#         return response



























