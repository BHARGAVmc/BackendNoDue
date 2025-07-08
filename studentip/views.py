from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
from rest_framework import status
from core.models import Student

class UpdateStudentDetailsView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        student = Student.objects.filter(email=email).first()

        if not student or not check_password(password, student.password):
            return Response({"error": "Invalid email or password"}, status=status.HTTP_400_BAD_REQUEST)

        # Update only these fields
        student.roll_no = request.data.get('roll_no', student.roll_no)
        student.branch = request.data.get('branch', student.branch)
        student.year = request.data.get('year', student.year)
        student.sem = request.data.get('sem', student.sem)
        student.section = request.data.get('section', student.section)
        student.save()

        return Response({"message": "Student details updated successfully."}, status=status.HTTP_200_OK)
