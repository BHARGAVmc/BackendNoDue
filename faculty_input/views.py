# faculty_input/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import FacultySubject
from .serializers import FacultySubjectSerializer
from core.models import Faculty

@api_view(['POST'])
def save_faculty_subject(request):
    email = request.data.get('email')

    if not email:
        return Response({'error': 'Email is required'}, status=400)

    try:
        faculty = Faculty.objects.get(email=email)
    except Faculty.DoesNotExist:
        return Response({'error': 'Faculty with this email does not exist'}, status=400)

    # ✅ Update Faculty with all fields from request
    faculty.fname = request.data.get('fname', faculty.fname)
    faculty.branch = request.data.get('branch', faculty.branch)
    faculty.year = request.data.get('year', faculty.year)
    faculty.sem = request.data.get('sem', faculty.sem)
    faculty.section = request.data.get('section', faculty.section)
    faculty.subject_code = request.data.get('course_code', faculty.subject_code)
    faculty.subject = request.data.get('subject', faculty.subject)
    faculty.save()

    # ✅ Create FacultySubject entry
    data = {
        'faculty': faculty.id,
        'branch': request.data.get('branch'),
        'year': request.data.get('year'),
        'sem': request.data.get('sem'),
        'section': request.data.get('section'),
        'course_code': request.data.get('course_code'),
        'subject': request.data.get('subject'),
    }

    serializer = FacultySubjectSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Faculty updated and data saved successfully'}, status=200)
    return Response(serializer.errors, status=400)
