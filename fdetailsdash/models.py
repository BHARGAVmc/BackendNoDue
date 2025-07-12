from django.db import models
from facultydash.models import FacultySubject
from core.models import Student

class StudentRequirementStatus(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    faculty_subject = models.ForeignKey(FacultySubject, on_delete=models.CASCADE)
    requirement_type = models.CharField(max_length=100)  # e.g., Assignment 1, NPTEL
    is_completed = models.BooleanField(default=False)
    remarks = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('student', 'faculty_subject', 'requirement_type')

    def __str__(self):
        return f"{self.student.roll_no} - {self.requirement_type} ({'✔' if self.is_completed else '✘'})"

# # File: fdetailsdash/models.py
# from django.db import models
# from core.models import Student
# from core.models import ChecklistItem
# from facultydash.models import FacultySubject

# class StudentChecklistStatus(models.Model):
#     roll = models.CharField(max_length=20)
#     remarks = models.TextField(blank=True, null=True)

# class StudentItemStatus(models.Model):
#     student = models.ForeignKey(StudentChecklistStatus, related_name='items', on_delete=models.CASCADE)
#     item = models.ForeignKey(ChecklistItem, on_delete=models.CASCADE)
#     checked = models.BooleanField(default=False)

# class StudentRequirementStatus(models.Model):
#     student = models.ForeignKey(Student, on_delete=models.CASCADE)
#     faculty_subject = models.ForeignKey(FacultySubject, on_delete=models.CASCADE)
#     requirement_type = models.CharField(max_length=100)  # e.g., Assignment 1, NPTEL
#     is_completed = models.BooleanField(default=False)
#     remarks = models.TextField(blank=True, null=True)

#     class Meta:
#         unique_together = ('student', 'faculty_subject', 'requirement_type')

#     def _str_(self):
#         return f"{self.student.roll_no} - {self.requirement_type} ({'✔' if self.is_completed else '✘'})"