from django.urls import path
from .views import UpdateStudentDetailsView

urlpatterns = [
    path('update/', UpdateStudentDetailsView.as_view(), name='update-student'),
]
