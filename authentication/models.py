# from django.db import models
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# class CustomUserManager(BaseUserManager):
#     def create_user(self, email, password=None, role='student', **extra_fields):
#         if not email:
#             raise ValueError('Email is required')
#         email = self.normalize_email(email)
#         user = self.model(email=email, role=role, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, password, role='admin', **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         return self.create_user(email, password, role, **extra_fields)

# class CustomUser(AbstractBaseUser, PermissionsMixin):
#     ROLE_CHOICES = (
#         ('student', 'Student'),
#         ('faculty', 'Faculty'),
#         ('admin', 'Admin'),
#     )

#     email = models.EmailField(unique=True)
#     role = models.CharField(max_length=10, choices=ROLE_CHOICES)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)

#     objects = CustomUserManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['role']

#     def __str__(self):
#         return self.email


from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Optional: If you still want to keep a single login table, you can keep CustomUser.
# Otherwise, use Student and Faculty directly with AbstractBaseUser.

class Student(models.Model):
    role = models.CharField(max_length=10, default='student')
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    roll_no = models.CharField(max_length=20, null=True, blank=True)
    branch = models.CharField(max_length=50, null=True, blank=True)
    year = models.CharField(max_length=10, null=True, blank=True)
    sem = models.CharField(max_length=10, null=True, blank=True)
    section = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.email

class Faculty(models.Model):
    role = models.CharField(max_length=10, default='faculty')
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    branch = models.CharField(max_length=50, null=True, blank=True)
    year = models.CharField(max_length=10, null=True, blank=True)
    sem = models.CharField(max_length=10, null=True, blank=True)
    section = models.CharField(max_length=10, null=True, blank=True)
    subject_code = models.CharField(max_length=20, null=True, blank=True)
    subject = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.email
