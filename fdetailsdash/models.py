from django.db import models
from facultydash.models import FacultySubject
from core.models import Student

# class StudentRequirementStatus(models.Model):
#     student = models.ForeignKey(Student, on_delete=models.CASCADE)
#     faculty_subject = models.ForeignKey(FacultySubject, on_delete=models.CASCADE)
#     requirement_type = models.CharField(max_length=100)  # e.g., Assignment 1, NPTEL
#     is_completed = models.BooleanField(default=False)
#     remarks = models.TextField(blank=True, null=True)
#     certificate_file = models.FileField(upload_to='certificates/', null=True, blank=True)


#     class Meta:
#         unique_together = ('student', 'faculty_subject', 'requirement_type')

#     def __str__(self):
#         return f"{self.student.roll_no} - {self.requirement_type} ({'✔' if self.is_completed else '✘'})"

class StudentRequirementStatus(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    faculty_subject = models.ForeignKey(FacultySubject, on_delete=models.CASCADE)
    requirement_type = models.CharField(max_length=100)
    is_completed = models.BooleanField(default=False)
    remarks = models.TextField(blank=True, null=True)
    
    # Certificate additions
    certificate_file = models.FileField(upload_to='certificates/', null=True, blank=True)  # Keep for backward compatibility

    soft_copy_required = models.BooleanField(default=False)
    hard_copy_required = models.BooleanField(default=False)

    soft_copy_file = models.FileField(upload_to='certificates/soft/', null=True, blank=True)
    hard_copy_submitted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('student', 'faculty_subject', 'requirement_type')

    def __str__(self):
        return f"{self.student.roll_no} - {self.requirement_type} ({'✔' if self.is_completed else '✘'})"
