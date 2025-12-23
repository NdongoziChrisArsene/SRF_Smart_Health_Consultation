from rest_framework import serializers

# 1. Symptom Checker
class SymptomCheckerSerializer(serializers.Serializer):
    symptoms = serializers.CharField(max_length=1000, help_text="Describe the symptoms (comma-separated or plain text).")
    symptoms.swagger_example = "fever, cough, chest pain"

    def validate_symptoms(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Symptoms cannot be empty.")
        return value


# 2. Medical Summary
class MedicalSummarySerializer(serializers.Serializer):
    medical_history = serializers.CharField(max_length=5000, help_text="Full medical history text.")
    medical_history.swagger_example = "Patient has hypertension and is on medication. Previous surgery in 2018."

    def validate_medical_history(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Medical history cannot be empty.")
        return value


# 3. Doctor Recommendation
class DoctorRecommendationSerializer(serializers.Serializer):
    symptoms = serializers.CharField(max_length=1000, help_text="Symptoms to analyze for recommendation.")
    location = serializers.CharField(max_length=200, help_text="City, district or region.")
    symptoms.swagger_example = "shortness of breath, chest pain"
    location.swagger_example = "Kigali"

    def validate_symptoms(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Symptoms cannot be empty.")
        return value

    def validate_location(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Location cannot be empty.")
        return value





















































# from rest_framework import serializers

# # 1. Symptom Checker
# class SymptomCheckerSerializer(serializers.Serializer):
#     symptoms = serializers.CharField(max_length=1000, help_text="Describe the symptoms (comma-separated or plain text).")
#     symptoms.swagger_example = "fever, cough, chest pain"

#     def validate_symptoms(self, value):
#         value = value.strip()
#         if not value:
#             raise serializers.ValidationError("Symptoms cannot be empty.")
#         return value


# # 2. Medical Summary
# class MedicalSummarySerializer(serializers.Serializer):
#     medical_history = serializers.CharField(max_length=5000, help_text="Full medical history text.")
#     medical_history.swagger_example = "Patient has hypertension and is on medication. Previous surgery in 2018."

#     def validate_medical_history(self, value):
#         value = value.strip()
#         if not value:
#             raise serializers.ValidationError("Medical history cannot be empty.")
#         return value


# # 3. Doctor Recommendation
# class DoctorRecommendationSerializer(serializers.Serializer):
#     symptoms = serializers.CharField(max_length=1000, help_text="Symptoms to analyze for recommendation.")
#     location = serializers.CharField(max_length=200, help_text="City, district or region.")
#     symptoms.swagger_example = "shortness of breath, chest pain"
#     location.swagger_example = "Kigali"

#     def validate_symptoms(self, value):
#         value = value.strip()
#         if not value:
#             raise serializers.ValidationError("Symptoms cannot be empty.")
#         return value

#     def validate_location(self, value):
#         value = value.strip()
#         if not value:
#             raise serializers.ValidationError("Location cannot be empty.")
#         return value























































# from rest_framework import serializers


# # =====================================================
# # 1. Symptom Checker
# # =====================================================
# class SymptomCheckerSerializer(serializers.Serializer):
#     symptoms = serializers.CharField(
#         max_length=1000,
#         help_text="Describe the symptoms (comma-separated or plain text).",
#     )

#     symptoms.swagger_example = "fever, cough, chest pain"

#     def validate_symptoms(self, value):
#         value = value.strip()
#         if not value:
#             raise serializers.ValidationError("Symptoms cannot be empty.")
#         return value


# # =====================================================
# # 2. Medical Summary
# # =====================================================
# class MedicalSummarySerializer(serializers.Serializer):
#     medical_history = serializers.CharField(
#         max_length=5000,
#         help_text="Full medical history text.",
#     )

#     medical_history.swagger_example = (
#         "Patient has hypertension and is on medication. Previous surgery in 2018."
#     )

#     def validate_medical_history(self, value):
#         value = value.strip()
#         if not value:
#             raise serializers.ValidationError("Medical history cannot be empty.")
#         return value


# # =====================================================
# # 3. Doctor Recommendation
# # =====================================================
# class DoctorRecommendationSerializer(serializers.Serializer):
#     symptoms = serializers.CharField(
#         max_length=1000,
#         help_text="Symptoms to analyze for recommendation.",
#     )
#     location = serializers.CharField(
#         max_length=200,
#         help_text="City, district or region.",
#     )

#     symptoms.swagger_example = "shortness of breath, chest pain"
#     location.swagger_example = "Kigali"

#     def validate_symptoms(self, value):
#         value = value.strip()
#         if not value:
#             raise serializers.ValidationError("Symptoms cannot be empty.")
#         return value

#     def validate_location(self, value):
#         value = value.strip()
#         if not value:
#             raise serializers.ValidationError("Location cannot be empty.")
#         return value
