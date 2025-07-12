# facultydash/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from facultydash.models import FacultySubject
from core.models import Faculty
from facultydash.serializers import FacultySubjectSerializer
from rest_framework import status
from django.contrib.auth.hashers import check_password  # ✅ Import for password checking


class FacultyLoginSubjectList(APIView):
    def get(self, request):
        """Test method to fetch first faculty's subject data"""
        faculty = Faculty.objects.first()
        if not faculty:
            return Response({"error": "No faculty found."}, status=404)

        subjects = FacultySubject.objects.filter(faculty=faculty)
        serializer = FacultySubjectSerializer(subjects, many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        """Login using email and password to fetch subjects"""
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({"error": "Email and password are required."}, status=400)

        try:
            faculty = Faculty.objects.get(email=email)
        except Faculty.DoesNotExist:
            return Response({"error": "Invalid email"}, status=401)

        # ✅ Use check_password to verify hashed password
        if not check_password(password, faculty.password):
            return Response({"error": "Invalid password"}, status=401)

        # ✅ Return subjects handled by the logged-in faculty
        subjects = FacultySubject.objects.filter(faculty=faculty)
        serializer = FacultySubjectSerializer(subjects, many=True)
        return Response(serializer.data, status=200)
