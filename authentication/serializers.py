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
from core.models import Student, Faculty,Login
from django.contrib.auth.hashers import make_password


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Login
        fields = ['email', 'password', 'role']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['email', 'password', 'role', 'roll_no', 'branch', 'year', 'sem', 'section']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return Student.objects.create(**validated_data)

class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ['email', 'password', 'role', 'branch', 'year', 'sem', 'section', 'subject_code', 'subject']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return Faculty.objects.create(**validated_data)
