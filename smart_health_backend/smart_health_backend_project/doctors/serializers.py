from rest_framework import serializers
from .models import DoctorProfile, Availability


class DoctorSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = DoctorProfile
        fields = [
            "id",
            "username",
            "email",
            "specialization",
            "location",
            "years_of_experience",
        ]
        read_only_fields = ("id", "username", "email")


class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = ["id", "day_of_week", "start_time", "end_time"]
        read_only_fields = ["id"]

    def validate(self, data):
        doctor = self.context.get("doctor")
        if not doctor:
            raise serializers.ValidationError("Doctor profile is required.")
        return data













































# from rest_framework import serializers
# from .models import Doctor, Availability


# class DoctorSerializer(serializers.ModelSerializer):
#     username = serializers.CharField(source="user.username", read_only=True)
#     email = serializers.CharField(source="user.email", read_only=True)

#     class Meta:
#         model = Doctor
#         fields = [
#             "id", "username", "email",
#             "specialization", "location", "years_of_experience"
#         ]
#         read_only_fields = ["id", "username", "email"]


# class AvailabilitySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Availability
#         fields = ["id", "day_of_week", "start_time", "end_time"]
#         read_only_fields = ["id"]

#     def validate(self, data):
#         doctor = self.context.get("doctor")
#         if not doctor:
#             raise serializers.ValidationError("Doctor profile is required.")
#         return data

