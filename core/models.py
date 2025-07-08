from django.db import models

class Login(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    role = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.email} ({self.role})"

class Student(models.Model):
    role = models.CharField(max_length=10, default='student')
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    roll_no = models.CharField(max_length=20, null=True, blank=True)
    branch = models.CharField(max_length=50, null=True, blank=True)
    year = models.CharField(max_length=10, null=True, blank=True)
    sem = models.CharField(max_length=10, null=True, blank=True)
    section = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.email

class Faculty(models.Model):
    role = models.CharField(max_length=10, default='faculty')
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    fname = models.CharField(max_length=100, null=True, blank=True)
    branch = models.CharField(max_length=50, null=True, blank=True)
    year = models.CharField(max_length=10, null=True, blank=True)
    sem = models.CharField(max_length=10, null=True, blank=True)
    section = models.CharField(max_length=10, null=True, blank=True)
    subject_code = models.CharField(max_length=20, null=True, blank=True)
    subject = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.email} - {self.fname or 'No Name'}"
