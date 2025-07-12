# facilty_input/serializers.py
# from rest_framework import serializers
# from .models import FacultySubject

# class FacultySubjectSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = FacultySubject
#         fields = '__all__'
from rest_framework import serializers

from facultydash.models import FacultySubject

from core.models import Faculty



class FacultySubjectSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(write_only=True)



    class Meta:

        model = FacultySubject

        fields = ['email', 'branch', 'year', 'semester', 'section', 'subject_code', 'subject_name']



    def create(self, validated_data):

        email = validated_data.pop('email')

        try:

            faculty = Faculty.objects.get(email=email)

        except Faculty.DoesNotExist:

            raise serializers.ValidationError("Faculty with this email does not exist")



        return FacultySubject.objects.create(faculty=faculty, **validated_data)