from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
from core.models import Student, Faculty

class StudentDashboardSubjectsView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        role = request.data.get('role')

        student = Student.objects.filter(email=email, role=role).first()
        if not student or not check_password(password, student.password):
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

        branch = student.branch
        year = student.year
        sem = student.sem
        section = student.section

        faculty_qs = Faculty.objects.filter(
            branch=branch,
            year=year,
            sem=sem,
            section=section
        )

        if not faculty_qs.exists():
            return Response({"message": "No subjects found"}, status=status.HTTP_404_NOT_FOUND)

        # ✅ Detailed subject list
        subjects = []
        for fac in faculty_qs:
            subjects.append({
                "subject_name": fac.subject,
                "subject_code": fac.subject_code,
                "faculty_name": fac.fname
            })

        return Response({
            "branch": branch,
            "year": year,
            "sem": sem,
            "section": section,
            "subjects": subjects
        }, status=status.HTTP_200_OK)

