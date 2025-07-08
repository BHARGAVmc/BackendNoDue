from django.urls import path
from .views import SendOTP, VerifyOTP, ResetPassword

urlpatterns = [
    path('send-otp/', SendOTP.as_view()),
    path('verify-otp/', VerifyOTP.as_view()),
    path('reset-password/', ResetPassword.as_view()),

]
