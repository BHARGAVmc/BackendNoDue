# # File: fdetailsdash/views.py
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from core.models import ChecklistItem
# from .models import StudentChecklistStatus, StudentItemStatus
# from .serializers import ChecklistItemSerializer, StudentChecklistStatusSerializer

# class ChecklistItemView(APIView):
#     def get(self, request):
#         items = ChecklistItem.objects.all()
#         serializer = ChecklistItemSerializer(items, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = ChecklistItemSerializer(data=request.data)
#         if serializer.is_valid():
#             item = serializer.save()
#             students = StudentChecklistStatus.objects.all()
#             for student in students:
#                 StudentItemStatus.objects.create(student=student, item=item, checked=False)
#             return Response({'message': 'Item added for all students'}, status=201)
#         return Response(serializer.errors, status=400)

# class ChecklistItemDeleteView(APIView):
#     def delete(self, request, pk):
#         try:
#             item = ChecklistItem.objects.get(pk=pk)
#             item.delete()
#             return Response({'message': 'Item deleted'}, status=204)
#         except ChecklistItem.DoesNotExist:
#             return Response({'error': 'Item not found'}, status=404)

# class StudentChecklistView(APIView):
#     def get(self, request):
#         students = StudentChecklistStatus.objects.all()
#         serializer = StudentChecklistStatusSerializer(students, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = StudentChecklistStatusSerializer(data=request.data, many=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'message': 'Saved successfully'}, status=201)
#         return Response(serializer.errors, status=400)

#     def put(self, request):
#         checklist_id = request.data.get('id')
#         if not checklist_id:
#             return Response({'error': 'Checklist ID is required'}, status=400)

#         try:
#             student_checklist = StudentChecklistStatus.objects.get(id=checklist_id)
#         except StudentChecklistStatus.DoesNotExist:
#             return Response({'error': 'Checklist not found'}, status=404)

#         serializer = StudentChecklistStatusSerializer(student_checklist, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'message': 'Updated successfully'}, status=200)
#         return Response(serializer.errors, status=400)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from core.models import Student, Faculty
from facultydash.models import FacultySubject
from fdetailsdash.models import StudentRequirementStatus

@csrf_exempt
def get_student_data_and_requirements(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)

        email = data.get('email')
        branch = data.get('branch')
        year = data.get('year')
        semester = data.get('semester')
        section = data.get('section')

        if not all([email, branch, year, semester, section]):
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        # Get students
        students = Student.objects.filter(branch=branch, year=year, semester=semester, section=section)
        roll_nos = list(students.values_list('roll_no', flat=True))

        try:
            faculty = Faculty.objects.get(email=email)
        except Faculty.DoesNotExist:
            return JsonResponse({'error': 'Faculty not found'}, status=404)

        # Get subjects assigned to this faculty
        subjects = FacultySubject.objects.filter(
            faculty=faculty,
            branch=branch,
            year=year,
            semester=semester,
            section=section
        )

        all_data = []

        for subject in subjects:
            # Get distinct requirement types for this subject
            requirement_types = StudentRequirementStatus.objects.filter(
                faculty_subject=subject
            ).values_list('requirement_type', flat=True).distinct()

            for student in students:
                for req_type in requirement_types:
                    # Try to fetch existing record
                    try:
                        req = StudentRequirementStatus.objects.get(
                            student=student,
                            faculty_subject=subject,
                            requirement_type=req_type
                        )
                        all_data.append({
                            'roll_no': student.roll_no,
                            'subject_code': subject.subject_code,
                            'subject_name': subject.subject_name,
                            'requirement_type': req_type,
                            'is_completed': req.is_completed,
                            'remarks': req.remarks,
                        })
                    except StudentRequirementStatus.DoesNotExist:
                        # If not found, mark incomplete
                        all_data.append({
                            'roll_no': student.roll_no,
                            'subject_code': subject.subject_code,
                            'subject_name': subject.subject_name,
                            'requirement_type': req_type,
                            'is_completed': False,
                            'remarks': ''
                        })

        return JsonResponse({
            'roll_numbers': roll_nos,
            'requirements': all_data
        })

    else:
        return JsonResponse({'error': 'Only POST method allowed'}, status=405)
    
@csrf_exempt
def add_requirement_for_class(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)

        email = data.get('email')
        branch = data.get('branch')
        year = data.get('year')
        semester = data.get('semester')
        section = data.get('section')
        requirement_type = data.get('requirement_type')
        remarks = data.get('remarks', '')

        if not all([email, branch, year, semester, section, requirement_type]):
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        # Get students in class
        students = Student.objects.filter(branch=branch, year=year, semester=semester, section=section)
        roll_nos = list(students.values_list('roll_no', flat=True))

        # Get faculty
        try:
            faculty = Faculty.objects.get(email=email)
        except Faculty.DoesNotExist:
            return JsonResponse({'error': 'Faculty not found'}, status=404)

        # Get ALL subjects mapped to this faculty for this class
        subjects = FacultySubject.objects.filter(
            faculty=faculty,
            branch=branch,
            year=year,
            semester=semester,
            section=section
        )

        if not subjects.exists():
            return JsonResponse({'error': 'No subjects found for this faculty and class'}, status=404)

        # Add requirement to each student for each subject
        for subject in subjects:
            for student in students:
                StudentRequirementStatus.objects.get_or_create(
                    student=student,
                    faculty_subject=subject,
                    requirement_type=requirement_type,
                    defaults={
                        'is_completed': False,
                        'remarks': remarks
                    }
                )

        # Reuse same logic to return updated data
        # Attach required POST keys to request manually to re-call
        request._body = json.dumps({
            'email': email,
            'branch': branch,
            'year': year,
            'semester': semester,
            'section': section
        })

        return get_student_data_and_requirements(request)

    else:
        return JsonResponse({'error': 'Only POST method allowed'}, status=405)


@csrf_exempt
def update_student_requirements(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            updates = data.get('updates', [])

            if not email or not updates:
                return JsonResponse({'error': 'Missing email or updates'}, status=400)

            try:
                faculty = Faculty.objects.get(email=email)
            except Faculty.DoesNotExist:
                return JsonResponse({'error': 'Faculty not found'}, status=404)

            for item in updates:
                roll_no = item.get('roll_no')
                subject_code = item.get('subject_code')
                requirement_type = item.get('requirement_type')
                is_completed = item.get('is_completed', False)
                remarks = item.get('remarks', '')

                try:
                    student = Student.objects.get(roll_no=roll_no)
                    faculty_subject = FacultySubject.objects.get(
                        faculty=faculty,
                        subject_code=subject_code
                    )

                    # Update or create the requirement
                    obj, created = StudentRequirementStatus.objects.update_or_create(
                        student=student,
                        faculty_subject=faculty_subject,
                        requirement_type=requirement_type,
                        defaults={
                            'is_completed': is_completed,
                            'remarks': remarks
                        }
                    )

                except (Student.DoesNotExist, FacultySubject.DoesNotExist):
                    continue  # Skip invalid entries

            return JsonResponse({'success': True, 'message': 'Requirements updated successfully'})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

    return JsonResponse({'error': 'Only POST method allowed'}, status=405)

@csrf_exempt
def delete_requirement_for_class(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        email = data.get('email')
        branch = data.get('branch')
        year = data.get('year')
        semester = data.get('semester')
        section = data.get('section')
        requirement_type = data.get('requirement_type')

        if not all([email, branch, year, semester, section, requirement_type]):
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        try:
            faculty = Faculty.objects.get(email=email)
        except Faculty.DoesNotExist:
            return JsonResponse({'error': 'Faculty not found'}, status=404)

        subjects = FacultySubject.objects.filter(
            faculty=faculty,
            branch=branch,
            year=year,
            semester=semester,
            section=section
        )

        count = 0
        for subject in subjects:
            deleted, _ = StudentRequirementStatus.objects.filter(
                faculty_subject=subject,
                requirement_type=requirement_type
            ).delete()
            count += deleted

        return JsonResponse({'message': 'Requirement deleted', 'deleted': count})

    return JsonResponse({'error': 'Only POST method allowed'}, status=405)
