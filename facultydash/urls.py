# facultydash/urls.py
from django.urls import path
from .views import FacultyLoginSubjectList

urlpatterns = [
    path('faculty-login/', FacultyLoginSubjectList.as_view(), name='faculty_login'),
]