import os
import sys

# FIXED: Remove .py from the settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import django
django.setup()

from accounts.models import CustomUser

print("=" * 60)
print("FINAL USER CREATION")
print("=" * 60)

# Delete all users
count = CustomUser.objects.count()
CustomUser.objects.all().delete()
print(f"✅ Deleted {count} users")

# Create users
users = [
    ('admin@test.com', 'admin', 'admin123', 'admin'),
    ('hr@test.com', 'hruser', 'hr123', 'hr'),
    ('employee@test.com', 'employee', 'emp123', 'employee'),
    ('umer@company.com', 'umer', '123456', 'admin'),
    ('salar@company.com', 'salar', '123456', 'hr'),
    ('faris@company.com', 'faris', '123456', 'employee'),
]

created_count = 0
for email, username, password, role in users:
    try:
        if role == 'admin':
            user = CustomUser.objects.create_superuser(email, username, password)
        else:
            user = CustomUser.objects.create_user(email, username, password, role=role)
        
        user.department = 'IT' if role == 'admin' else 'HR' if role == 'hr' else 'Engineering'
        user.clearance_level = 3 if role == 'admin' else 2 if role == 'hr' else 1
        user.location = 'Office' if role in ['admin', 'hr'] else 'Remote'
        user.employee_type = 'fulltime'
        user.is_active = True
        user.is_staff = True
        user.save()
        created_count += 1
        print(f"✅ Created: {email} ({role}) with password: {password}")
    except Exception as e:
        print(f"❌ Error creating {email}: {e}")

print("\n" + "=" * 60)
print(f"✅ {created_count} users created successfully!")
print("=" * 60)
print("\n📋 Login Credentials:")
print("  Admin    : admin@test.com / admin123")
print("  HR       : hr@test.com / hr123")
print("  Employee : employee@test.com / emp123")
print("  Umer     : umer@company.com / 123456")
print("  Salar    : salar@company.com / 123456")
print("  Faris    : faris@company.com / 123456")
print("\n" + "=" * 60)