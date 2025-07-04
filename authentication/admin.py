# # from django.contrib import admin

# # Register your models here.
# # from django.contrib import admin
# # from django.contrib.auth.admin import UserAdmin
# # from .models import CustomUser

# # admin.site.register(CustomUser, UserAdmin)
# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# # from .models import CustomUser

# class CustomUserAdmin(UserAdmin):
#     model = CustomUser
#     list_display = ('email', 'role', 'is_staff', 'is_active')
#     list_filter = ('role', 'is_staff', 'is_active')
#     search_fields = ('email',)
#     ordering = ('email',)
    
#     fieldsets = (
#         (None, {'fields': ('email', 'password', 'role')}),
#         ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
#     )

#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email', 'role', 'password1', 'password2', 'is_staff', 'is_active')}
#         ),
#     )

# # admin.site.register(CustomUser, CustomUserAdmin)


from django.contrib import admin
from .models import Student, Faculty  # Make sure these are defined in your models.py

admin.site.register(Student)
admin.site.register(Faculty)
