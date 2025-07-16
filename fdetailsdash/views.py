# from django.views.decorators.http import require_POST
# from django.utils.decorators import method_decorator
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import json
# from core.models import Student, Faculty
# from facultydash.models import FacultySubject
# from fdetailsdash.models import StudentRequirementStatus
# from django.http import FileResponse, Http404

# @csrf_exempt
# def get_student_data_and_requirements(request):
#     if request.method == 'POST':
#         import json
#         data = json.loads(request.body)

#         email = data.get('email')
#         branch = data.get('branch')
#         year = data.get('year')
#         semester = data.get('semester')
#         section = data.get('section')

#         if not all([email, branch, year, semester, section]):
#             return JsonResponse({'error': 'Missing required fields'}, status=400)

#         # Get students
#         students = Student.objects.filter(branch=branch, year=year, semester=semester, section=section)
#         roll_nos = list(students.values_list('roll_no', flat=True))

#         try:
#             faculty = Faculty.objects.get(email=email)
#         except Faculty.DoesNotExist:
#             return JsonResponse({'error': 'Faculty not found'}, status=404)

#         # Get subjects assigned to this faculty
#         subjects = FacultySubject.objects.filter(
#             faculty=faculty,
#             branch=branch,
#             year=year,
#             semester=semester,
#             section=section
#         )

#         all_data = []

#         for subject in subjects:
#             # Get distinct requirement types for this subject
#             requirement_types = StudentRequirementStatus.objects.filter(
#                 faculty_subject=subject
#             ).values_list('requirement_type', flat=True).distinct()

#             for student in students:
#                 for req_type in requirement_types:
#                     # Try to fetch existing record
#                     try:
#                         req = StudentRequirementStatus.objects.get(
#                             student=student,
#                             faculty_subject=subject,
#                             requirement_type=req_type
#                         )
#                         all_data.append({
#                             'roll_no': student.roll_no,
#                             'subject_code': subject.subject_code,
#                             'subject_name': subject.subject_name,
#                             'requirement_type': req_type,
#                             'is_completed': req.is_completed,
#                             'remarks': req.remarks,
#                         })
#                     except StudentRequirementStatus.DoesNotExist:
#                         # If not found, mark incomplete
#                         all_data.append({
#                             'roll_no': student.roll_no,
#                             'subject_code': subject.subject_code,
#                             'subject_name': subject.subject_name,
#                             'requirement_type': req_type,
#                             'is_completed': False,
#                             'remarks': ''
#                         })

#         return JsonResponse({
#             'roll_numbers': roll_nos,
#             'requirements': all_data
#         })

#     else:
#         return JsonResponse({'error': 'Only POST method allowed'}, status=405)
    
# @csrf_exempt
# def add_requirement_for_class(request):
#     if request.method == 'POST':
#         import json
#         data = json.loads(request.body)

#         email = data.get('email')
#         branch = data.get('branch')
#         year = data.get('year')
#         semester = data.get('semester')
#         section = data.get('section')
#         requirement_type = data.get('requirement_type')
#         remarks = data.get('remarks', '')

#         if not all([email, branch, year, semester, section, requirement_type]):
#             return JsonResponse({'error': 'Missing required fields'}, status=400)

#         # Get students in class
#         students = Student.objects.filter(branch=branch, year=year, semester=semester, section=section)
#         roll_nos = list(students.values_list('roll_no', flat=True))

#         # Get faculty
#         try:
#             faculty = Faculty.objects.get(email=email)
#         except Faculty.DoesNotExist:
#             return JsonResponse({'error': 'Faculty not found'}, status=404)

#         # Get ALL subjects mapped to this faculty for this class
#         subjects = FacultySubject.objects.filter(
#             faculty=faculty,
#             branch=branch,
#             year=year,
#             semester=semester,
#             section=section
#         )

#         if not subjects.exists():
#             return JsonResponse({'error': 'No subjects found for this faculty and class'}, status=404)

#         # Add requirement to each student for each subject
#         for subject in subjects:
#             for student in students:
#                 StudentRequirementStatus.objects.get_or_create(
#                     student=student,
#                     faculty_subject=subject,
#                     requirement_type=requirement_type,
#                     defaults={
#                         'is_completed': False,
#                         'remarks': remarks
#                     }
#                 )

#         # Reuse same logic to return updated data
#         # Attach required POST keys to request manually to re-call
#         request._body = json.dumps({
#             'email': email,
#             'branch': branch,
#             'year': year,
#             'semester': semester,
#             'section': section
#         })

#         return get_student_data_and_requirements(request)

#     else:
#         return JsonResponse({'error': 'Only POST method allowed'}, status=405)


# @csrf_exempt
# def update_student_requirements(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             email = data.get('email')
#             updates = data.get('updates', [])

#             if not email or not updates:
#                 return JsonResponse({'error': 'Missing email or updates'}, status=400)

#             try:
#                 faculty = Faculty.objects.get(email=email)
#             except Faculty.DoesNotExist:
#                 return JsonResponse({'error': 'Faculty not found'}, status=404)

#             for item in updates:
#                 roll_no = item.get('roll_no')
#                 subject_code = item.get('subject_code')
#                 requirement_type = item.get('requirement_type')
#                 is_completed = item.get('is_completed', False)
#                 remarks = item.get('remarks', '')

#                 try:
#                     student = Student.objects.get(roll_no=roll_no)
#                     faculty_subject = FacultySubject.objects.get(
#                         faculty=faculty,
#                         subject_code=subject_code
#                     )

#                     # Update or create the requirement
#                     obj, created = StudentRequirementStatus.objects.update_or_create(
#                         student=student,
#                         faculty_subject=faculty_subject,
#                         requirement_type=requirement_type,
#                         defaults={
#                             'is_completed': is_completed,
#                             'remarks': remarks
#                         }
#                     )

#                 except (Student.DoesNotExist, FacultySubject.DoesNotExist):
#                     continue  # Skip invalid entries

#             return JsonResponse({'success': True, 'message': 'Requirements updated successfully'})

#         except json.JSONDecodeError:
#             return JsonResponse({'error': 'Invalid JSON'}, status=400)

#     return JsonResponse({'error': 'Only POST method allowed'}, status=405)

# @csrf_exempt
# def delete_requirement_for_class(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)

#         email = data.get('email')
#         branch = data.get('branch')
#         year = data.get('year')
#         semester = data.get('semester')
#         section = data.get('section')
#         requirement_type = data.get('requirement_type')

#         if not all([email, branch, year, semester, section, requirement_type]):
#             return JsonResponse({'error': 'Missing required fields'}, status=400)

#         try:
#             faculty = Faculty.objects.get(email=email)
#         except Faculty.DoesNotExist:
#             return JsonResponse({'error': 'Faculty not found'}, status=404)

#         subjects = FacultySubject.objects.filter(
#             faculty=faculty,
#             branch=branch,
#             year=year,
#             semester=semester,
#             section=section
#         )

#         count = 0
#         for subject in subjects:
#             deleted, _ = StudentRequirementStatus.objects.filter(
#                 faculty_subject=subject,
#                 requirement_type=requirement_type
#             ).delete()
#             count += deleted

#         return JsonResponse({'message': 'Requirement deleted', 'deleted': count})

#     return JsonResponse({'error': 'Only POST method allowed'}, status=405)
# @csrf_exempt
# @require_POST
# def upload_certificate(request):
#     roll_no = request.POST.get('roll_no')
#     subject_code = request.POST.get('subject_code')
#     requirement_type = request.POST.get('requirement_type')
#     email = request.POST.get('email')  # faculty email

#     certificate_file = request.FILES.get('certificate_file')

#     if not all([roll_no, subject_code, requirement_type, email, certificate_file]):
#         return JsonResponse({'error': 'Missing required fields'}, status=400)

#     try:
#         student = Student.objects.get(roll_no=roll_no)
#         faculty = Faculty.objects.get(email=email)
#         faculty_subject = FacultySubject.objects.get(faculty=faculty, subject_code=subject_code)

#         req_status, created = StudentRequirementStatus.objects.get_or_create(
#             student=student,
#             faculty_subject=faculty_subject,
#             requirement_type=requirement_type
#         )

#         req_status.certificate_file = certificate_file
#         req_status.save()

#         return JsonResponse({'success': True, 'message': 'Certificate uploaded successfully'})
#     except (Student.DoesNotExist, Faculty.DoesNotExist, FacultySubject.DoesNotExist):
#         return JsonResponse({'error': 'Invalid student or subject or faculty'}, status=404)
# from django.http import FileResponse, Http404

# @csrf_exempt
# def get_certificate(request):
#     roll_no = request.GET.get("roll_no")
#     subject_code = request.GET.get("subject_code")
#     requirement_type = request.GET.get("requirement_type")

#     try:
#         student = Student.objects.get(roll_no=roll_no)
#         faculty_subject = FacultySubject.objects.get(subject_code=subject_code)
#         record = StudentRequirementStatus.objects.get(
#             student=student,
#             faculty_subject=faculty_subject,
#             requirement_type=requirement_type
#         )

#         if not record.certificate_file:
#             raise Http404("Certificate not uploaded.")

#         return FileResponse(record.certificate_file.open(), content_type="application/pdf")

#     except Exception as e:
#         raise Http404(str(e))


from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.http import JsonResponse, FileResponse, Http404
from django.views.decorators.csrf import csrf_exempt
import json

from core.models import Student, Faculty
from facultydash.models import FacultySubject
from fdetailsdash.models import StudentRequirementStatus

@csrf_exempt
def get_student_data_and_requirements(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        email = data.get('email')
        branch = data.get('branch')
        year = data.get('year')
        semester = data.get('semester')
        section = data.get('section')

        if not all([email, branch, year, semester, section]):
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        students = Student.objects.filter(branch=branch, year=year, semester=semester, section=section)
        roll_nos = list(students.values_list('roll_no', flat=True))

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

        all_data = []

        for subject in subjects:
            requirement_types = StudentRequirementStatus.objects.filter(
                faculty_subject=subject
            ).values_list('requirement_type', flat=True).distinct()

            for student in students:
                for req_type in requirement_types:
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
                            'soft_copy_required': req.soft_copy_required,
                            'hard_copy_required': req.hard_copy_required,
                            'soft_copy_uploaded': bool(req.soft_copy_file),
                            'hard_copy_submitted': req.hard_copy_submitted,
                        })
                    except StudentRequirementStatus.DoesNotExist:
                        all_data.append({
                            'roll_no': student.roll_no,
                            'subject_code': subject.subject_code,
                            'subject_name': subject.subject_name,
                            'requirement_type': req_type,
                            'is_completed': False,
                            'remarks': '',
                            'soft_copy_required': False,
                            'hard_copy_required': False,
                            'soft_copy_uploaded': False,
                            'hard_copy_submitted': False,
                        })

        return JsonResponse({
            'roll_numbers': roll_nos,
            'requirements': all_data
        })

    return JsonResponse({'error': 'Only POST method allowed'}, status=405)


@csrf_exempt
def add_requirement_for_class(request):
    if request.method == 'POST':
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

        students = Student.objects.filter(branch=branch, year=year, semester=semester, section=section)
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

        soft_required = data.get('soft_copy_required', False)
        hard_required = data.get('hard_copy_required', False)

        for subject in subjects:
            for student in students:
                StudentRequirementStatus.objects.get_or_create(
                    student=student,
                    faculty_subject=subject,
                    requirement_type=requirement_type,
                    defaults={
                        'is_completed': False,
                        'remarks': remarks,
                        'soft_copy_required': soft_required,
                        'hard_copy_required': hard_required
                    }
                )

        request._body = json.dumps({
            'email': email,
            'branch': branch,
            'year': year,
            'semester': semester,
            'section': section
        })

        return get_student_data_and_requirements(request)

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

            faculty = Faculty.objects.get(email=email)

            for item in updates:
                roll_no = item.get('roll_no')
                subject_code = item.get('subject_code')
                requirement_type = item.get('requirement_type')
                is_completed = item.get('is_completed', False)
                remarks = item.get('remarks', '')

                student = Student.objects.get(roll_no=roll_no)
                faculty_subject = FacultySubject.objects.get(
                    faculty=faculty,
                    subject_code=subject_code
                )

                StudentRequirementStatus.objects.update_or_create(
                    student=student,
                    faculty_subject=faculty_subject,
                    requirement_type=requirement_type,
                    defaults={
                        'is_completed': is_completed,
                        'remarks': remarks
                    }
                )

            return JsonResponse({'success': True, 'message': 'Requirements updated successfully'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

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

        faculty = Faculty.objects.get(email=email)

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


# @csrf_exempt
# @require_POST
# def upload_certificate_v2(request):
#     roll_no = request.POST.get('roll_no')
#     subject_code = request.POST.get('subject_code')
#     requirement_type = request.POST.get('requirement_type')
#     email = request.POST.get('email')
#     upload_type = request.POST.get('upload_type')  # soft or hard

#     try:
#         student = Student.objects.get(roll_no=roll_no)
#         faculty = Faculty.objects.get(email=email)
#         faculty_subject = FacultySubject.objects.get(faculty=faculty, subject_code=subject_code)

#         req = StudentRequirementStatus.objects.get(
#             student=student,
#             faculty_subject=faculty_subject,
#             requirement_type=requirement_type
#         )

#         if upload_type == 'soft':
#             file = request.FILES.get('certificate_file') 
#             if not file:
#                 return JsonResponse({'error': 'Missing soft copy file'}, status=400)
#             req.soft_copy_file = file
#         elif upload_type == 'hard':
#             req.hard_copy_submitted = True
#         else:
#             return JsonResponse({'error': 'Invalid upload_type'}, status=400)

#         req.save()
#         return JsonResponse({'success': True, 'message': 'Upload updated'})

#     except Exception as e:
#         return JsonResponse({'error': str(e)}, status=400)
@csrf_exempt
@require_POST
def upload_certificate_v2(request):
    roll_no = request.POST.get('roll_no')
    subject_code = request.POST.get('subject_code')
    requirement_type = request.POST.get('requirement_type')
    email = request.POST.get('email')
    upload_type = request.POST.get('upload_type')  # "soft" or "hard"

    try:
        student = Student.objects.get(roll_no=roll_no)
        faculty = Faculty.objects.get(email=email)
        faculty_subject = FacultySubject.objects.get(faculty=faculty, subject_code=subject_code)

        req = StudentRequirementStatus.objects.get(
            student=student,
            faculty_subject=faculty_subject,
            requirement_type=requirement_type
        )

        if upload_type == 'soft':
            file = request.FILES.get('certificate_file')  
            if not file:
                return JsonResponse({'error': 'Missing soft copy file'}, status=400)

            req.soft_copy_file = file
            req.is_completed = True  
        elif upload_type == 'hard':
            req.hard_copy_submitted = True
            req.is_completed = True  
        else:
            return JsonResponse({'error': 'Invalid upload_type'}, status=400)

        req.save()
        return JsonResponse({'success': True, 'message': 'Upload successful', 'filename': file.name if upload_type == 'soft' else ''})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)



@csrf_exempt
def update_certificate_requirement_type(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        email = data.get('email')
        subject_code = data.get('subject_code')
        requirement_type = data.get('requirement_type')
        soft = data.get('soft_copy_required')
        hard = data.get('hard_copy_required')

        try:
            faculty = Faculty.objects.get(email=email)
            faculty_subject = FacultySubject.objects.get(faculty=faculty, subject_code=subject_code)

            reqs = StudentRequirementStatus.objects.filter(
                faculty_subject=faculty_subject,
                requirement_type=requirement_type
            )

            for req in reqs:
                req.soft_copy_required = soft
                req.hard_copy_required = hard
                req.save()

            return JsonResponse({'success': True, 'message': 'Certificate requirement type updated'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Only POST method allowed'}, status=405)


@csrf_exempt
def get_certificate(request):
    roll_no = request.GET.get("roll_no")
    subject_code = request.GET.get("subject_code")
    requirement_type = request.GET.get("requirement_type")

    try:
        student = Student.objects.get(roll_no=roll_no)
        faculty_subject = FacultySubject.objects.get(subject_code=subject_code)
        record = StudentRequirementStatus.objects.get(
            student=student,
            faculty_subject=faculty_subject,
            requirement_type=requirement_type
        )

        if not record.soft_copy_file:
            raise Http404("Soft copy not uploaded.")

        return FileResponse(record.soft_copy_file.open(), content_type="application/pdf")

    except Exception as e:
        raise Http404(str(e))
