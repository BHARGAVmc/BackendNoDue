# facilty_input/serializers.py
from rest_framework import serializers
from .models import FacultySubject

class FacultySubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacultySubject
        fields = '__all__'
