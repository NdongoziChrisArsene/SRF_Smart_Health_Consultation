from rest_framework.permissions import BasePermission


class IsPatient(BasePermission):
    """
    Allows access only to users with a patient profile.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, "patient_profile")


class IsDoctor(BasePermission):
    """
    Allows access only to users with a doctor profile.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, "doctor_profile")


class IsAdmin(BasePermission):
    """
    Allows access only to admin/superuser.
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            (request.user.is_staff or request.user.role == "admin")
        )

# class IsAdminUserForReports(BasePermission):
#     """
#     Only Admin users can access reporting endpoints.
#     Prevents doctors and patients from viewing system-wide analytics.
#     """

#     message = "You do not have permission to access system reports."
    
#     def has_permission(self, request, view):
#         return request.user.is_authenticated and request.user.is_staff
    
    
