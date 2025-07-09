from django.db import models
from core.models import Faculty

class FacultySubject(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='subject_mappings')
    branch = models.CharField(max_length=100)
    year = models.CharField(max_length=10)
    semester = models.CharField(max_length=10)
    section = models.CharField(max_length=10)
    subject_code = models.CharField(max_length=20)
    subject_name = models.CharField(max_length=100)

    class Meta:
        unique_together = ('faculty', 'branch', 'year', 'semester', 'section', 'subject_code')

    def __str__(self):
        return f"{self.subject_code} - {self.subject_name} ({self.branch}-{self.year}-{self.semester}-{self.section})"
