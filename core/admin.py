#admin.py
from django.contrib import admin
from .models import Student, Faculty, Login

admin.site.register(Student)
admin.site.register(Faculty)
admin.site.register(Login)
