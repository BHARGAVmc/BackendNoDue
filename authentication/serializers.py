# from rest_framework import serializers
# from .models import CustomUser

# class SignupSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ['email', 'password', 'role']
#         extra_kwargs = {'password': {'write_only': True}}

#     def create(self, validated_data):
#         return CustomUser.objects.create_user(**validated_data)
    
from rest_framework import serializers
from .models import Student, Faculty

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['email', 'password', 'role', 'roll_no', 'branch', 'year', 'sem', 'section']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # You can add password hashing if needed here
        return Student.objects.create(**validated_data)

class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ['email', 'password', 'role', 'branch', 'year', 'sem', 'section', 'subject_code', 'subject']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return Faculty.objects.create(**validated_data)
