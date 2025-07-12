from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import FacultySubjectSerializer
from core.models import Faculty
from facultydash.models import FacultySubject

@api_view(['POST'])
def save_faculty_subject(request):
    email = request.data.get('email')  # static email from frontend

    if not email:
        return Response({'error': 'Email is required'}, status=400)

    try:
        faculty = Faculty.objects.get(email=email)
    except Faculty.DoesNotExist:
        return Response({'error': 'Faculty not found'}, status=400)

    faculty.fname = request.data.get('fname', faculty.fname)
    faculty.save()

    data = {
        'email': email,
        'branch': request.data.get('branch'),
        'year': request.data.get('year'),
        'semester': request.data.get('semester'),
        'section': request.data.get('section'),
        'subject_code': request.data.get('subject_code'),
        'subject_name': request.data.get('subject_name'),
    }

    serializer = FacultySubjectSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Faculty subject mapping saved successfully'}, status=200)

    return Response(serializer.errors, status=400)