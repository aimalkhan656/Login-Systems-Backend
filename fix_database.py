import os
import sys
import subprocess

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("=" * 60)
print("Fixing Database Issues")
print("=" * 60)

# Step 1: Delete database
if os.path.exists('db.sqlite3'):
    os.remove('db.sqlite3')
    print("✅ Deleted db.sqlite3")

# Step 2: Delete migration files
migrations_dir = 'accounts/migrations'
if os.path.exists(migrations_dir):
    for file in os.listdir(migrations_dir):
        if file != '__init__.py' and file.endswith('.py'):
            os.remove(os.path.join(migrations_dir, file))
            print(f"✅ Deleted {file}")

# Step 3: Make migrations
print("\n📌 Creating migrations...")
subprocess.run(['python', 'manage.py', 'makemigrations', 'accounts'])

# Step 4: Migrate
print("\n📌 Applying migrations...")
subprocess.run(['python', 'manage.py', 'migrate'])

print("\n" + "=" * 60)
print("✅ Database fixed!")
print("=" * 60)
print("\nNow run:")
print("  python manage.py createsuperuser")
print("  python create_users.py")