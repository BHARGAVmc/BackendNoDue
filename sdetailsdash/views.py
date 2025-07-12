from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password

from core.models import Student
from facultydash.models import FacultySubject
from fdetailsdash.models import StudentRequirementStatus

class StudentDashboardSubjectsView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({"error": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        # Step 1: Authenticate student
        student = Student.objects.filter(email=email).first()
        if not student or not check_password(password, student.password):
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

        # Step 2: Get student details
        roll_no = student.roll_no
        branch = student.branch
        year = student.year
        semester = student.semester     # ✅ updated here
        section = student.section

        # Step 3: Get matching faculty subjects
        faculty_subjects = FacultySubject.objects.filter(
            branch=branch,
            year=year,
            semester=semester,          # ✅ updated here
            section=section
        )

        if not faculty_subjects.exists():
            return Response({"message": "No subjects found"}, status=status.HTTP_404_NOT_FOUND)

        # Step 4: Loop through subjects and get requirement status
        result = []
        for fac_sub in faculty_subjects:
            faculty = fac_sub.faculty
            faculty_email = faculty.email

            # Get requirements for this student and subject
            requirement_entries = StudentRequirementStatus.objects.filter(
                student=student,
                faculty_subject=fac_sub
            )

            requirements = []
            for req in requirement_entries:
                requirements.append({
                    "requirement_type": req.requirement_type,
                    "is_completed": req.is_completed,
                    "remarks": req.remarks
                })

            result.append({
                "subject_code": fac_sub.subject_code,
                "subject_name": fac_sub.subject_name,
                "faculty_name": faculty.fname,
                "faculty_email": faculty_email,
                "requirements": requirements
            })

        # Step 5: Return all data
        return Response({
            "student": {
                "roll_no": roll_no,
                "branch": branch,
                "year": year,
                "semester": semester,
                "section": section
            },
            "subjects": result
        }, status=status.HTTP_200_OK)
