# # from django.shortcuts import render

# # # Create your views here.
# # from rest_framework.response import Response
# # from rest_framework.decorators import api_view

# # @api_view(['GET'])
# # def home(request):
# #     return Response({"message": "Welcome to Authentication API"})

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .models import Student, Faculty
# from .serializers import StudentSerializer, FacultySerializer
# # from .serializers import SignupSerializer
# # from django.db import IntegrityError
# # from django.contrib.auth import authenticate
# # from .models import CustomUser

# class SignupView(APIView):
#     def post(self, request):
#         role = request.data.get('role')

#         if role == 'student':
#             serializer = StudentSerializer(data=request.data)
#         elif role == 'faculty':
#             serializer = FacultySerializer(data=request.data)
#         else:
#             return Response({"error": "Invalid role"}, status=status.HTTP_400_BAD_REQUEST)

#         if serializer.is_valid():
#             user = serializer.save()
#             return Response({
#                 "message": f"{role.capitalize()} created successfully",
#                 "user": {
#                     "email": user.email,
#                     "role": user.role
#                 }
#             }, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class LoginView(APIView):
#     def post(self, request):
#         email = request.data.get("email")
#         password = request.data.get("password")

#         if email is None or password is None:
#             return Response({"error": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)

#         user = authenticate(request, email=email, password=password)

#         if user is not None:
#             return Response({
#                 "message": "Login successful",
#                 "role": user.role
#             }, status=status.HTTP_200_OK)
#         else:
#             return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.models import Student, Faculty, Login
from .serializers import StudentSerializer, FacultySerializer, LoginSerializer
from rest_framework.permissions import AllowAny
from django.db import IntegrityError
from django.contrib.auth.hashers import check_password
from rest_framework.authentication import BasicAuthentication, SessionAuthentication

class SignupView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        role = request.data.get('role')
        email = request.data.get('email')

        # First: Insert into Login table
        login_serializer = LoginSerializer(data=request.data)
        if not login_serializer.is_valid():
            return Response(login_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            login_serializer.save()
        except IntegrityError:
            return Response({"error": "Email already exists. Try logging in."}, status=status.HTTP_400_BAD_REQUEST)

        if role == 'student':
            serializer = StudentSerializer(data=request.data)
        elif role == 'faculty':
            serializer = FacultySerializer(data=request.data)
        else:
            return Response({"error": "Invalid role"}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": f"{role.capitalize()} created successfully",
                "user": {
                    "email": user.email,
                    "role": user.role
                }
            }, status=status.HTTP_201_CREATED)

        else:
            Login.objects.filter(email=email).delete()
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not all([email, password]):
            return Response({"error": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            login_user = Login.objects.get(email=email)
        except Login.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        if not check_password(password, login_user.password):
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        role = login_user.role

        try:
            if role == "student":
                user = Student.objects.get(email=email)

                if not all([user.roll_no, user.branch, user.year, user.semester, user.section]):
                    return Response({
                        "message": "Incomplete student profile",
                        "user": {
                            "email": user.email,
                            "role": role
                        },
                        "profile_complete": False
                    }, status=status.HTTP_200_OK)

            elif role == "faculty":
                user = Faculty.objects.get(email=email)

            else:
                return Response({"error": "Invalid role in Login table"}, status=status.HTTP_400_BAD_REQUEST)

            return Response({
                "message": "Login successful",
                "user": {
                    "email": user.email,
                    "role": role
                },
                "profile_complete": True
            }, status=status.HTTP_200_OK)

        except (Student.DoesNotExist, Faculty.DoesNotExist):
            return Response({"error": "Login entry found but profile missing"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
