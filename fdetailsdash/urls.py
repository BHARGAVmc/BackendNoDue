from django.urls import path
from .views import get_student_data_and_requirements,add_requirement_for_class,update_student_requirements,delete_requirement_for_class

urlpatterns = [
    path('get-student-details/', get_student_data_and_requirements),
    path('add-requirement/', add_requirement_for_class),
     path('update-requirements/',update_student_requirements), 
      path('delete-requirement/', delete_requirement_for_class),
]
