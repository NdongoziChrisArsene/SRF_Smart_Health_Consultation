from appointments.models import Appointment
from payments.models import Payment
from django.contrib.auth import get_user_model
from django.db.models import Sum
from datetime import date

User = get_user_model()


class AnalyticsService:
    @staticmethod
    def appointment_stats(start: date, end: date) -> dict:
        qs = Appointment.objects.filter(created_at__range=[start, end])

        return {
            "total": qs.count(),
            "completed": qs.filter(status="completed").count(),
            "cancelled": qs.filter(status="cancelled").count(),
            "pending": qs.filter(status="pending").count(),
        }

    @staticmethod
    def financial_stats(start: date, end: date) -> dict:
        total = (
            Payment.objects
            .filter(timestamp__range=[start, end])
            .aggregate(total=Sum("amount"))["total"]
            or 0
        )
        return {"total_revenue": total}

    @staticmethod
    def user_activity_stats(start: date, end: date) -> dict:
        return {
            "new_users": User.objects.filter(date_joined__range=[start, end]).count(),
            "active_users": User.objects.filter(last_login__range=[start, end]).count(),
        }


















































# from appointments.models import Appointment
# from payments.models import Payment
# from django.contrib.auth import get_user_model
# from django.db.models import Sum
# from datetime import date

# User = get_user_model()


# class AnalyticsService:
#     @staticmethod
#     def appointment_stats(start: date, end: date) -> dict:
#         qs = Appointment.objects.filter(created_at__range=[start, end])
#         return {
#             "total": qs.count(),
#             "completed": qs.filter(status=Appointment.STATUS_COMPLETED).count(),
#             "cancelled": qs.filter(status=Appointment.STATUS_CANCELLED).count(),
#             "pending": qs.filter(status=Appointment.STATUS_PENDING).count(),
#         }

#     @staticmethod
#     def financial_stats(start: date, end: date) -> dict:
#         total = (
#             Payment.objects
#             .filter(timestamp__range=[start, end])
#             .aggregate(total=Sum("amount"))["total"]
#             or 0
#         )
#         return {"total_revenue": total}

#     @staticmethod
#     def user_activity_stats(start: date, end: date) -> dict:
#         return {
#             "new_users": User.objects.filter(date_joined__range=[start, end]).count(),
#             "active_users": User.objects.filter(last_login__range=[start, end]).count(),
#         }




































# from appointments.models import Appointment
# from payments.models import Payment
# from django.contrib.auth import get_user_model
# from django.db.models import Sum
# from datetime import date, datetime

# User = get_user_model()

# class AnalyticsService:
#     @staticmethod
#     def appointment_stats(start: date, end: date) -> dict:
#         """
#         Returns counts of appointments by status in the given date range.
#         """
#         qs = Appointment.objects.filter(created_at__range=[start, end])
#         return {
#             "total": qs.count(),
#             "completed": qs.filter(status=Appointment.STATUS_COMPLETED).count(),
#             "cancelled": qs.filter(status=Appointment.STATUS_CANCELLED).count(),
#             "pending": qs.filter(status=Appointment.STATUS_PENDING).count(),
#         }

#     @staticmethod
#     def financial_stats(start: date, end: date) -> dict:
#         """
#         Returns total revenue in the given date range.
#         """
#         qs = Payment.objects.filter(timestamp__range=[start, end])
#         total_amount = qs.aggregate(total=Sum("amount"))["total"] or 0
#         return {"total_revenue": total_amount}

#     @staticmethod
#     def user_activity_stats(start: date, end: date) -> dict:
#         """
#         Returns counts of new and active users in the given date range.
#         """
#         return {
#             "new_users": User.objects.filter(date_joined__range=[start, end]).count(),
#             "active_users": User.objects.filter(last_login__range=[start, end]).count(),
#         }








































# from appointments.models import Appointment
# from payments.models import Payment
# from django.contrib.auth import get_user_model

# User = get_user_model()

# class AnalyticsService:
#     @staticmethod
#     def appointment_stats(start, end):
#         qs = Appointment.objects.filter(created_at__range=[start, end])
#         return {
#             "total": qs.count(),
#             "completed": qs.filter(status="completed").count(),
#             "cancelled": qs.filter(status="cancelled").count(),
#             "pending": qs.filter(status="pending").count(),
#         }

#     @staticmethod
#     def financial_stats(start, end):
#         qs = Payment.objects.filter(timestamp__range=[start, end])
#         total_amount = qs.aggregate(total=models.Sum("amount"))["total"]
#         return {"total_revenue": total_amount or 0}

#     @staticmethod
#     def user_activity_stats(start, end):
#         return {
#             "new_users": User.objects.filter(date_joined__range=[start, end]).count(),
#             "active_users": User.objects.filter(last_login__range=[start, end]).count(),
#         }
