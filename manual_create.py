import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

print("Deleting all users...")
User.objects.all().delete()

print("Creating users...")

# Create each user with try/except
users = [
    ('admin@test.com', 'admin', 'admin123', True),
    ('hr@test.com', 'hruser', 'hr123', False),
    ('employee@test.com', 'employee', 'emp123', False),
    ('umer@company.com', 'umer', '123456', True),
    ('salar@company.com', 'salar', '123456', False),
    ('faris@company.com', 'faris', '123456', False),
]

for email, username, password, is_super in users:
    try:
        if is_super:
            user = User.objects.create_superuser(email, username, password)
        else:
            user = User.objects.create_user(email, username, password)
            if email == 'hr@test.com' or email == 'salar@company.com':
                user.role = 'hr'
            else:
                user.role = 'employee'
        user.is_staff = True
        user.is_active = True
        user.save()
        print(f"✅ {email} created with password: {password}")
    except Exception as e:
        print(f"❌ Error with {email}: {e}")

print("\nAll users:")
for user in User.objects.all():
    print(f"  {user.email} - {user.role} - Staff: {user.is_staff}")