# from rest_framework.permissions import BasePermission


# class IsDoctor(BasePermission):
#     """
#     Allows access only for users who have a doctor_profile.
#     """

#     def has_permission(self, request, view):
#         return request.user.is_authenticated and hasattr(request.user, "doctor_profile")

