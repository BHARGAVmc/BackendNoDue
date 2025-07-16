from django.urls import path
# from .views import get_student_data_and_requirements,add_requirement_for_class,update_student_requirements,delete_requirement_for_class,upload_certificate,get_certificate

# urlpatterns = [
#     path('get-student-details/', get_student_data_and_requirements),
#     path('add-requirement/', add_requirement_for_class),
#      path('update-requirements/',update_student_requirements), 
#       path('delete-requirement/', delete_requirement_for_class),
#       path('upload-certificate/', upload_certificate),
#       path('get-certificate/', get_certificate, name='get_certificate'),

# ]

from .views import (
    get_student_data_and_requirements,
    add_requirement_for_class,
    update_student_requirements,
    delete_requirement_for_class,
    upload_certificate_v2,
    get_certificate,
    update_certificate_requirement_type
)

urlpatterns = [
    path('get-student-details/', get_student_data_and_requirements),
    path('add-requirement/', add_requirement_for_class),
    path('update-requirements/', update_student_requirements),
    path('delete-requirement/', delete_requirement_for_class),
    path('upload-certificate-v2/', upload_certificate_v2),
    path('get-certificate/', get_certificate),
    path('update-certificate-type/', update_certificate_requirement_type),
]
