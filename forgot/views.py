## forgot/views.py
import random
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.models import Student, Faculty
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

otp_store = {}  # key: email, value: otp



@method_decorator(csrf_exempt, name='dispatch')
class SendOTP(APIView):
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        otp = str(random.randint(100000, 999999))
        otp_store[email] = otp

        try:
            send_mail(
                subject='Your OTP Code',
                message=f'Your OTP is {otp}',
                from_email=None,
                recipient_list=[email],
                fail_silently=False,
            )
        except Exception as e:
            return Response({"error": f"Failed to send email: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"message": "OTP sent successfully"}, status=status.HTTP_200_OK)



class VerifyOTP(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')

        if not email or not otp:
            return Response({"error": "Email and OTP are required"}, status=status.HTTP_400_BAD_REQUEST)

        if otp_store.get(email) == otp:
            return Response({"message": "OTP verified successfully"}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)


class ResetPassword(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')

        if not all([email, password, confirm_password]):
            return Response(
                {"error": "Email, password, and confirm_password are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if password != confirm_password:
            return Response(
                {"error": "Passwords do not match"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Search for user in Student or Faculty
        user = Student.objects.filter(email=email).first()
        if not user:
            user = Faculty.objects.filter(email=email).first()

        if not user:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        user.password = make_password(password)
        user.save()

        return Response({"message": "Password reset successful"}, status=status.HTTP_200_OK)