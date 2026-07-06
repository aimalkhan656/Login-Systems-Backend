import os
import sys
import subprocess
import shutil

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

print("=" * 70)
print("FIXING EVERYTHING - RUN THIS ONCE")
print("=" * 70)

# 1. Delete database
if os.path.exists('db.sqlite3'):
    os.remove('db.sqlite3')
    print("✅ Deleted db.sqlite3")

# 2. Delete migrations
migrations_dir = 'accounts/migrations'
if os.path.exists(migrations_dir):
    for f in os.listdir(migrations_dir):
        if f != '__init__.py' and f.endswith('.py'):
            os.remove(os.path.join(migrations_dir, f))
            print(f"✅ Deleted {f}")
    
    cache_dir = os.path.join(migrations_dir, '__pycache__')
    if os.path.exists(cache_dir):
        shutil.rmtree(cache_dir)
        print("✅ Deleted __pycache__")

# 3. Ensure __init__.py exists
init_file = os.path.join(migrations_dir, '__init__.py')
if not os.path.exists(init_file):
    with open(init_file, 'w') as f:
        f.write('')
    print("✅ Created __init__.py")

# 4. Run migrations
print("\n📌 Running migrations...")
subprocess.run(['python', 'manage.py', 'makemigrations', 'accounts'], check=False)
subprocess.run(['python', 'manage.py', 'migrate'], check=False)

# 5. Create users using subprocess
print("\n📌 Creating users...")
subprocess.run([
    'python', 'manage.py', 'shell', '-c',
    'from accounts.models import CustomUser; '
    'CustomUser.objects.all().delete(); '
    'CustomUser.objects.create_superuser("admin@test.com", "admin", "admin123"); '
    'CustomUser.objects.create_user("hr@test.com", "hruser", "hr123", role="hr"); '
    'CustomUser.objects.create_user("employee@test.com", "employee", "emp123", role="employee"); '
    'CustomUser.objects.create_superuser("umer@company.com", "umer", "123456"); '
    'CustomUser.objects.create_user("salar@company.com", "salar", "123456", role="hr"); '
    'CustomUser.objects.create_user("faris@company.com", "faris", "123456", role="employee"); '
    'print("All users created successfully!")'
], check=False)

print("\n" + "=" * 70)
print("✅ COMPLETE!")
print("=" * 70)
print("\n📋 LOGIN CREDENTIALS:")
print("  Admin    : admin@test.com / admin123")
print("  HR       : hr@test.com / hr123")
print("  Employee : employee@test.com / emp123")
print("  Umer     : umer@company.com / 123456")
print("  Salar    : salar@company.com / 123456")
print("  Faris    : faris@company.com / 123456")
print("\n🚀 Now run: python manage.py runserver")
print("=" * 70)