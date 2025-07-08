## core/urls.py
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),
    path('otp/',include('otp.urls')),
    path('fpassword/',include('forgot.urls')),
    path('f_input/', include('faculty_input.urls')),
]
