from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
from rest_framework import status
from core.models import Student

class UpdateStudentDetailsView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({"error": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        student = Student.objects.filter(email=email).first()

        if not student:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

        if not check_password(password, student.password):
            return Response({"error": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST)

        # Update only the fields if they are provided
        student.roll_no = request.data.get('roll_no', student.roll_no)
        student.branch = request.data.get('branch', student.branch)
        student.year = request.data.get('year', student.year)
        student.semester = request.data.get('semester', student.semester)
        student.section = request.data.get('section', student.section)

        student.save()

        return Response({
            "message": "Student details updated successfully.",
            "updated_data": {
                "roll_no": student.roll_no,
                "branch": student.branch,
                "year": student.year,
                "semester": student.semester,
                "section": student.section
            }
        }, status=status.HTTP_200_OK)
