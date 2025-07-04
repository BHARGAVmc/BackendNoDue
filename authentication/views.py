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


# # class SignupView(APIView):
# #     def post(self, request):
# #         serializer = SignupSerializer(data=request.data)
# #         if serializer.is_valid():
# #             try:
# #                 user = serializer.save()
# #                 return Response({
# #                     "message": "User created successfully",
# #                     "user": {
# #                         "id": user.id,
# #                         "email": user.email,
# #                         "role": user.role
# #                     }
# #                 }, status=status.HTTP_201_CREATED)
# #             except IntegrityError:
# #                 return Response(
# #                     {"error": "A user with this email already exists."},
# #                     status=status.HTTP_400_BAD_REQUEST
# #                 )
# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

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
from .models import Student, Faculty
from .serializers import StudentSerializer, FacultySerializer
from rest_framework.permissions import AllowAny
from rest_framework.authentication import BasicAuthentication, SessionAuthentication

class SignupView(APIView):
    authentication_classes = []  # Disable default auth
    permission_classes = [AllowAny]

    def post(self, request):
        role = request.data.get('role')

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
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    authentication_classes = []  # Disable default auth
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        role = request.data.get("role")

        if not all([email, password, role]):
            return Response({"error": "Email, password, and role are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            if role == "student":
                user = Student.objects.get(email=email, password=password)
            elif role == "faculty":
                user = Faculty.objects.get(email=email, password=password)
            else:
                return Response({"error": "Invalid role"}, status=status.HTTP_400_BAD_REQUEST)

            return Response({
                "message": "Login successful",
                "user": {
                    "email": user.email,
                    "role": user.role
                }
            }, status=status.HTTP_200_OK)

        except (Student.DoesNotExist, Faculty.DoesNotExist):
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
