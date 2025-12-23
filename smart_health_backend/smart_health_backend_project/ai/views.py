from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle, ScopedRateThrottle
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import logging

from .serializers import (
    SymptomCheckerSerializer,
    MedicalSummarySerializer,
    DoctorRecommendationSerializer,
)
from .gemini_utils import ( 
    call_gemini,  
)
from doctors.models import DoctorProfile  # ✅ Use DoctorProfile instead of Doctor

logger = logging.getLogger("ai")


# --------------------------------------------------
# Base AI View
# --------------------------------------------------
class BaseAIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [UserRateThrottle, ScopedRateThrottle]
    throttle_scope = "ai"
    http_method_names = ["post"]

    def format_response(self, data=None, message="", status_type="success",
                        http_status=status.HTTP_200_OK):
        return Response(
            {"status": status_type, "message": message, "data": data},
            status=http_status
        )


# --------------------------------------------------
# 1. AI Symptom Checker
# --------------------------------------------------
class AISymptomCheckerView(BaseAIView):
    serializer_class = SymptomCheckerSerializer

    @swagger_auto_schema(
        operation_summary="AI Symptom Checker",
        request_body=SymptomCheckerSerializer,
        responses={200: "Symptom analysis result"}
    )
    def post(self, request, *args, **kwargs):
        logger.info(f"Symptom checker called by user {request.user.id}")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = call_gemini(f"Analyze these symptoms: {serializer.validated_data['symptoms']}")

        return self.format_response(
            data={"analysis": result},
            message="Symptom analysis completed."
        )


# --------------------------------------------------
# 2. AI Medical Summary
# --------------------------------------------------
class AIMedicalSummaryView(BaseAIView):
    serializer_class = MedicalSummarySerializer

    @swagger_auto_schema(
        operation_summary="AI Medical Summary",
        request_body=MedicalSummarySerializer,
        responses={200: "Medical summary result"}
    )
    def post(self, request, *args, **kwargs):
        logger.info(f"Medical summary called by user {request.user.id}")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        summary = call_gemini(f"Generate a medical summary: {serializer.validated_data['medical_history']}")

        return self.format_response(
            data={"summary": summary},
            message="Medical summary generated."
        )


# --------------------------------------------------
# 3. AI Doctor Recommendation
# --------------------------------------------------
class AIDoctorRecommendationView(BaseAIView):
    serializer_class = DoctorRecommendationSerializer

    @swagger_auto_schema(
        operation_summary="AI Doctor Recommendation",
        request_body=DoctorRecommendationSerializer,
        responses={200: "Doctor recommendation output"}
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        symptoms = serializer.validated_data["symptoms"]
        location = serializer.validated_data["location"]

        doctors = DoctorProfile.objects.filter(location__icontains=location)

        if not doctors.exists():
            return self.format_response(
                data=[],
                message="No doctors available in this location.",
                status_type="error",
                http_status=status.HTTP_404_NOT_FOUND
            )

        recommendation = call_gemini(
            f"Recommend doctors for symptoms '{symptoms}' in location '{location}' from list: {[d.user.username for d in doctors]}"
        )

        return self.format_response(
            data={"recommendation": recommendation},
            message="Doctor recommendation generated."
        )

















































# from rest_framework import generics, permissions, status
# from rest_framework.response import Response
# from rest_framework.throttling import UserRateThrottle, ScopedRateThrottle
# from drf_yasg.utils import swagger_auto_schema
# from drf_yasg import openapi
# import logging

# from .serializers import (
#     SymptomCheckerSerializer,
#     MedicalSummarySerializer,
#     DoctorRecommendationSerializer,
# )
# from .gemini_utils import (
#     ai_symptom_checker,
#     ai_medical_summary,
#     ai_doctor_recommendation,
# )
# from doctors.models import Doctor

# logger = logging.getLogger("ai")


# # --------------------------------------------------
# # Base AI View
# # --------------------------------------------------
# class BaseAIView(generics.GenericAPIView):
#     permission_classes = [permissions.IsAuthenticated]
#     throttle_classes = [UserRateThrottle, ScopedRateThrottle]
#     throttle_scope = "ai" 
#     http_method_names = ["post"]

#     def format_response(self, data=None, message="", status_type="success",
#                         http_status=status.HTTP_200_OK):
#         return Response(
#             {"status": status_type, "message": message, "data": data},
#             status=http_status
#         )


# # --------------------------------------------------
# # 1. AI Symptom Checker
# # --------------------------------------------------
# class AISymptomCheckerView(BaseAIView):
#     serializer_class = SymptomCheckerSerializer

#     @swagger_auto_schema(
#         operation_summary="AI Symptom Checker",
#         request_body=SymptomCheckerSerializer,
#         responses={200: "Symptom analysis result"}
#     )
#     def post(self, request, *args, **kwargs):
#         logger.info(f"Symptom checker called by user {request.user.id}")

#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         result = ai_symptom_checker(serializer.validated_data["symptoms"])

#         if not result:
#             logger.warning(f"Empty AI symptom response for user {request.user.id}")


#         return self.format_response(
#             data={"analysis": result},
#             message="Symptom analysis completed."
#         )


# # --------------------------------------------------
# # 2. AI Medical Summary
# # --------------------------------------------------
# class AIMedicalSummaryView(BaseAIView):
#     serializer_class = MedicalSummarySerializer

#     @swagger_auto_schema(
#         operation_summary="AI Medical Summary",
#         request_body=MedicalSummarySerializer,
#         responses={200: "Medical summary result"}
#     )
#     def post(self, request, *args, **kwargs):
#         logger.info(f"Medical summary called by user {request.user.id}")

#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         summary = ai_medical_summary(serializer.validated_data["medical_history"])

#         return self.format_response(
#             data={"summary": summary},
#             message="Medical summary generated."
#         )


# # --------------------------------------------------
# # 3. AI Doctor Recommendation
# # --------------------------------------------------
# class AIDoctorRecommendationView(BaseAIView):
#     serializer_class = DoctorRecommendationSerializer

#     @swagger_auto_schema(
#         operation_summary="AI Doctor Recommendation",
#         request_body=DoctorRecommendationSerializer,
#         responses={200: "Doctor recommendation output"}
#     )
#     def post(self, request, *args, **kwargs):

#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         symptoms = serializer.validated_data["symptoms"]
#         location = serializer.validated_data["location"]

#         doctors = Doctor.objects.filter(location__icontains=location)

#         if not doctors.exists():
#             return self.format_response(
#                 data=[],
#                 message="No doctors available in this location.",
#                 status_type="error",
#                 http_status=status.HTTP_404_NOT_FOUND
#             )

#         recommendation = ai_doctor_recommendation(symptoms, location, doctors)

#         return self.format_response(
#             data={"recommendation": recommendation},
#             message="Doctor recommendation generated."
#         )
