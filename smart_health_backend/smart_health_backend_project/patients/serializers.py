from rest_framework import serializers
from .models import PatientProfile


class PatientSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = PatientProfile
        fields = (
            "id",
            "username",
            "email",
            "age",
            "gender",
            "medical_history",
        )


class UpdatePatientSerializer(serializers.ModelSerializer):
    medical_history = serializers.CharField(
        allow_blank=True,
        allow_null=True,
        required=False,
    )

    class Meta:
        model = PatientProfile
        fields = ("age", "gender", "medical_history")
































# from rest_framework import serializers
# from .models import PatientProfile


# class PatientSerializer(serializers.ModelSerializer):
#     username = serializers.CharField(source="user.username", read_only=True)
#     email = serializers.CharField(source="user.email", read_only=True)

#     class Meta:
#         model = PatientProfile
#         fields = [
#             "id",
#             "username",
#             "email",
#             "age",
#             "gender",
#             "medical_history",
#         ]


# class UpdatePatientSerializer(serializers.ModelSerializer):
#     medical_history = serializers.CharField(
#         allow_blank=True,
#         allow_null=True,
#         required=False
#     )

#     class Meta:
#         model = PatientProfile
#         fields = ["age", "gender", "medical_history"]




































# from rest_framework import serializers
# from .models import Patient

# class PatientSerializer(serializers.ModelSerializer):
#     username = serializers.CharField(source="user.username", read_only=True)
#     email = serializers.CharField(source="user.email", read_only=True)

#     class Meta:
#         model = Patient
#         fields = [
#             "id",
#             "username",
#             "email",
#             "age",
#             "gender",
#             "medical_history",
#         ]


# class UpdatePatientSerializer(serializers.ModelSerializer):
#     medical_history = serializers.CharField(allow_blank=True, allow_null=True, required=False)

#     class Meta:
#         model = Patient
#         fields = ["age", "gender", "medical_history"]





























# from rest_framework import serializers    
# from .models import Patient           
# from users.models import User      

# class PatientSerializer(serializers.ModelSerializer): 
#     username = serializers.CharField(source="user.username", read_only=True)
#     email = serializers.CharField(source="user.email", read_only=True)
    
#     class Meta: 
#         model = Patient         
#         fields = [
#             'id',
#             'username',
#             'email',
#             'age',
#             'gender',
#             'medical_history'
#         ]
        
# class UpdatePatientSerializer(serializers.ModelSerializer): 
#     medical_history = serializers.CharField(allow_blank=True)
#     class Meta: 
#         model = Patient 
#         fields = ['age', 'gender', 'medical_history']
