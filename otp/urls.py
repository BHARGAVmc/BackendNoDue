from django.urls import path
from .views import send_otp

urlpatterns =[
    path('send/',send_otp),
]