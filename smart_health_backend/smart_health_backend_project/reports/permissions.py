from rest_framework.permissions import BasePermission


class IsAdminUserForReports(BasePermission):
    """
    Only Admin users can access reporting endpoints.
    Prevents doctors and patients from viewing system-wide analytics.
    """

    message = "You do not have permission to access system reports."
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_staff
    



















# from rest_framework.permissions import BasePermission


# class IsAdminUserForReports(BasePermission):
#     message = "Only admin users can access reports."

#     def has_permission(self, request, view):
#         return request.user.is_authenticated and request.user.is_staff


















# from rest_framework.permissions import BasePermission


# class IsAdminUserForReports(BasePermission):
#     """
#     Only Admin users can access reporting endpoints.
#     Prevents doctors and patients from viewing system-wide analytics.
#     """

#     message = "You do not have permission to access system reports."

#     def has_permission(self, request, view):
#         return request.user.is_authenticated and request.user.is_staff
