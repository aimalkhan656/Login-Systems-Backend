from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        return self.create_user(email, username, password, **extra_fields)

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('hr', 'HR'),
        ('employee', 'Employee'),
        ('manager', 'Manager'),
    ]
    
    # ===== RBAC Fields =====
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employee')
    
    # ===== ACL Fields =====
    email = models.EmailField(unique=True)
    is_super_admin = models.BooleanField(default=False)  # Only Umer
    
    # ===== ABAC Fields =====
    department = models.CharField(max_length=100, blank=True)
    clearance_level = models.IntegerField(default=1)  # 1=Low, 2=Medium, 3=High
    location = models.CharField(max_length=50, blank=True, default='Remote')
    employee_type = models.CharField(max_length=20, default='fulltime')
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return f"{self.email} ({self.role})"

class Document(models.Model):
    """For ABAC demonstration"""
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    department = models.CharField(max_length=100)
    clearance_required = models.IntegerField(default=1)
    is_confidential = models.BooleanField(default=False)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} (Dept: {self.department})"