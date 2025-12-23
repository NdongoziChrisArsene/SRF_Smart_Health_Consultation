from django.urls import path
from .views import GenerateReportView, DownloadReportView, ReportStatusView

urlpatterns = [
    path("generate/", GenerateReportView.as_view(), name="generate-report"),
    path("<int:pk>/download/", DownloadReportView.as_view(), name="download-report"),
    path("<int:pk>/status/", ReportStatusView.as_view(), name="report-status"),  # new endpoint
]





















# from django.urls import path
# from .views import GenerateReportView, DownloadReportView, ReportStatusView

# urlpatterns = [
#     path("generate/", GenerateReportView.as_view(), name="generate-report"),
#     path("<int:pk>/download/", DownloadReportView.as_view(), name="download-report"),
#     path("<int:pk>/status/", ReportStatusView.as_view(), name="report-status"),
# ]

























# from django.urls import path
# from .views import GenerateReportView, DownloadReportView, ReportStatusView

# urlpatterns = [
#     path("generate/", GenerateReportView.as_view(), name="generate-report"),
#     path("<int:pk>/download/", DownloadReportView.as_view(), name="download-report"),
#     path("<int:pk>/status/", ReportStatusView.as_view(), name="report-status"),  # NEW
# ]































# from django.urls import path
# from .views import GenerateReportView, DownloadReportView

# urlpatterns = [
#     path("generate/", GenerateReportView.as_view(), name="generate-report"),
#     path("<int:pk>/download/", DownloadReportView.as_view(), name="download-report"),
# ]


















# from django.urls import path
# from .views import GenerateReportView

# urlpatterns = [
#     path("generate/", GenerateReportView.as_view(), name="generate-report"),
# ]











