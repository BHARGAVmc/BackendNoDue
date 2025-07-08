from django.urls import path
from .views import StudentDashboardSubjectsView

urlpatterns = [
    path('subjects/', StudentDashboardSubjectsView.as_view(), name='student-dashboard-subjects'),
]
