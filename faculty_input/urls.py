# faculty_input/urls.py
from django.urls import path
from .views import save_faculty_subject

urlpatterns = [
    path('save-faculty-subject/', save_faculty_subject),
]
