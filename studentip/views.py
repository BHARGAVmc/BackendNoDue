# from rest_framework.views import APIView
# from rest_framework.response import Response
# from django.contrib.auth.hashers import check_password
# from rest_framework import status
# from core.models import Student

# class UpdateStudentDetailsView(APIView):
#     def post(self, request):
#         email = request.data.get('email')
#         password = request.data.get('password')

#         if not email or not password:
#             return Response({"error": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)

#         student = Student.objects.filter(email=email).first()

#         if not student:
#             return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

#         if not check_password(password, student.password):
#             return Response({"error": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST)

#         # Update only the fields if they are provided
#         student.roll_no = request.data.get('roll_no', student.roll_no)
#         student.branch = request.data.get('branch', student.branch)
#         student.year = request.data.get('year', student.year)
#         student.semester = request.data.get('semester', student.semester)
#         student.section = request.data.get('section', student.section)

#         student.save()

#         return Response({
#             "message": "Student details updated successfully.",
#             "updated_data": {
#                 "roll_no": student.roll_no,
#                 "branch": student.branch,
#                 "year": student.year,
#                 "semester": student.semester,
#                 "section": student.section
#             }
#         }, status=status.HTTP_200_OK)


# from rest_framework.views import APIView
# from rest_framework.response import Response
# from django.contrib.auth.hashers import check_password
# from rest_framework import status
# from core.models import Student
# from facultydash.models import FacultySubject
# from fdetailsdash.models import StudentRequirementStatus

# class UpdateStudentDetailsView(APIView):
#     def post(self, request):
#         email = request.data.get('email')
#         password = request.data.get('password')

#         if not email or not password:
#             return Response({"error": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)

#         student = Student.objects.filter(email=email).first()

#         if not student:
#             return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

#         if not check_password(password, student.password):
#             return Response({"error": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST)

#         # 🔄 Update student profile
#         student.roll_no = request.data.get('roll_no', student.roll_no)
#         student.branch = request.data.get('branch', student.branch)
#         student.year = request.data.get('year', student.year)
#         student.semester = request.data.get('semester', student.semester)
#         student.section = request.data.get('section', student.section)
#         student.save()

#         # 🔍 Get all subjects that match student's profile
#         matched_subjects = FacultySubject.objects.filter(
#             branch=student.branch,
#             year=student.year,
#             semester=student.semester,
#             section=student.section
#         )

#         created_count = 0

#         for subject in matched_subjects:
#             # ✅ Find requirements already created for this subject (by any other student)
#             existing_requirements = StudentRequirementStatus.objects.filter(
#                 faculty_subject=subject
#             ).values_list('requirement_type', flat=True).distinct()

#             for req_type in existing_requirements:
#                 # 🔄 Only add if this requirement is not already assigned to this student
#                 already_exists = StudentRequirementStatus.objects.filter(
#                     student=student,
#                     faculty_subject=subject,
#                     requirement_type=req_type
#                 ).exists()

#                 if not already_exists:
#                     StudentRequirementStatus.objects.create(
#                         student=student,
#                         faculty_subject=subject,
#                         requirement_type=req_type
#                     )
#                     created_count += 1

#         return Response({
#             "message": "Student details updated successfully.",
#             "requirements_assigned": created_count,
#             "updated_data": {
#                 "roll_no": student.roll_no,
#                 "branch": student.branch,
#                 "year": student.year,
#                 "semester": student.semester,
#                 "section": student.section
#             }
#         }, status=status.HTTP_200_OK)

from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
from rest_framework import status
from core.models import Student
from facultydash.models import FacultySubject
from fdetailsdash.models import StudentRequirementStatus

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

        #  Update student profile
        student.roll_no = request.data.get('roll_no', student.roll_no)
        student.branch = request.data.get('branch', student.branch)
        student.year = request.data.get('year', student.year)
        student.semester = request.data.get('semester', student.semester)
        student.section = request.data.get('section', student.section)
        student.save()

        #  Get all subjects matching student's academic profile
        matched_subjects = FacultySubject.objects.filter(
            branch=student.branch,
            year=student.year,
            semester=student.semester,
            section=student.section
        )

        created_count = 0  # Counter for how many requirements were created

        for subject in matched_subjects:
            #  Get all unique requirement types already assigned to this subject
            existing_requirements = StudentRequirementStatus.objects.filter(
                faculty_subject=subject
            ).values_list('requirement_type', flat=True).distinct()

            for req_type in existing_requirements:
                already_exists = StudentRequirementStatus.objects.filter(
                    student=student,
                    faculty_subject=subject,
                    requirement_type=req_type
                ).exists()

                if not already_exists:
                    # Defaults
                    soft_copy = False
                    hard_copy = False

                    #  If requirement is a certificate, copy soft/hard flags
                    if req_type.lower().endswith("certificate"):
                        example = StudentRequirementStatus.objects.filter(
                            faculty_subject=subject,
                            requirement_type=req_type
                        ).first()
                        if example:
                            soft_copy = example.soft_copy_required
                            hard_copy = example.hard_copy_required

                    #  Create new requirement status entry for this student
                    StudentRequirementStatus.objects.create(
                        student=student,
                        faculty_subject=subject,
                        requirement_type=req_type,
                        soft_copy_required=soft_copy,
                        hard_copy_required=hard_copy
                    )
                    created_count += 1

        return Response({
            "message": "Student details updated successfully.",
            "requirements_assigned": created_count,
            "updated_data": {
                "roll_no": student.roll_no,
                "branch": student.branch,
                "year": student.year,
                "semester": student.semester,
                "section": student.section
            }
        }, status=status.HTTP_200_OK)

