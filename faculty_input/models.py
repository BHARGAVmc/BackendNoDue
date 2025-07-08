from django.db import models
from core.models import Faculty  # ✅ make sure this works

class FacultySubject(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='subjects')
    branch = models.CharField(max_length=50)
    year = models.CharField(max_length=20)
    sem = models.CharField(max_length=10)
    section = models.CharField(max_length=10)
    course_code = models.CharField(max_length=50)
    subject = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.faculty.fname or self.faculty.email} - {self.subject}"
