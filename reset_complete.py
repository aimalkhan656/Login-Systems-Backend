import os
import sys
import shutil
import subprocess

print("=" * 60)
print("COMPLETE RESET - This WILL Work!")
print("=" * 60)

# 1. Delete database
if os.path.exists('db.sqlite3'):
    os.remove('db.sqlite3')
    print("✅ Deleted db.sqlite3")

# 2. Delete all migration files
migrations_dir = 'accounts/migrations'
if os.path.exists(migrations_dir):
    for file in os.listdir(migrations_dir):
        if file != '__init__.py':
            file_path = os.path.join(migrations_dir, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"✅ Deleted {file}")

# 3. Delete __pycache__
cache_dir = 'accounts/migrations/__pycache__'
if os.path.exists(cache_dir):
    shutil.rmtree(cache_dir)
    print("✅ Deleted __pycache__")

# 4. Make migrations
print("\n📌 Creating migrations...")
result = subprocess.run(['python', 'manage.py', 'makemigrations', 'accounts'], 
                        capture_output=True, text=True)
print(result.stdout)
if result.stderr:
    print(result.stderr)

# 5. Check what migrations were created
print("\n📌 Migration files:")
migrations = [f for f in os.listdir('accounts/migrations') if f.endswith('.py') and f != '__init__.py']
if migrations:
    for m in migrations:
        print(f"  - {m}")
else:
    print("  No migrations created!")

# 6. Apply migrations FORCEFULLY
print("\n📌 Applying migrations...")
result = subprocess.run(['python', 'manage.py', 'migrate'], 
                        capture_output=True, text=True)
print(result.stdout)
if result.stderr:
    print(result.stderr)

# 7. Check if table exists
print("\n📌 Checking if table exists...")
result = subprocess.run([
    'python', '-c', 
    'import os; os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings"); import django; django.setup(); from django.db import connection; tables = connection.introspection.table_names(); print("accounts_customuser" in tables)'
], capture_output=True, text=True)
print(f"Table exists: {result.stdout.strip()}")

print("\n" + "=" * 60)
print("✅ COMPLETE!")
print("=" * 60)