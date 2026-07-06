import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from accounts.models import CustomUser, Document
from datetime import datetime

print("=" * 60)
print("Creating Users for RBAC, ACL, and ABAC")
print("=" * 60)

# Delete all existing users and documents
CustomUser.objects.all().delete()
Document.objects.all().delete()
print("✅ Cleared existing users and documents")

# ========== RBAC USERS ==========
print("\n📌 Creating RBAC Users...")

# Admin
admin = CustomUser.objects.create_superuser(
    email='admin@test.com',
    username='admin',
    password='admin123'
)
admin.role = 'admin'
admin.department = 'IT'
admin.save()
print(f"✅ Admin created: admin@test.com / admin123")

# HR
hr = CustomUser.objects.create_user(
    email='hr@test.com',
    username='hruser',
    password='hr123',
    role='hr'
)
hr.department = 'HR'
hr.save()
print(f"✅ HR created: hr@test.com / hr123")

# Employee
emp = CustomUser.objects.create_user(
    email='employee@test.com',
    username='employee',
    password='emp123',
    role='employee'
)
emp.department = 'Engineering'
emp.save()
print(f"✅ Employee created: employee@test.com / emp123")

# ========== ACL USERS ==========
print("\n📌 Creating ACL Users...")

# Umer - Full Admin (ACL specific)
umer = CustomUser.objects.create_superuser(
    email='umer@company.com',
    username='umer',
    password='123456'
)
umer.role = 'admin'
umer.department = 'IT'
umer.clearance_level = 3
umer.location = 'Office'
umer.employee_type = 'fulltime'
umer.is_super_admin = True
umer.save()
print(f"✅ Umer (ACL Full Access): umer@company.com / 123456")

# Salar - HR (ACL specific)
salar = CustomUser.objects.create_user(
    email='salar@company.com',
    username='salar',
    password='123456',
    role='hr'
)
salar.department = 'HR'
salar.clearance_level = 2
salar.location = 'Office'
salar.employee_type = 'fulltime'
salar.save()
print(f"✅ Salar (ACL HR): salar@company.com / 123456")

# Faris - Employee (ACL specific)
faris = CustomUser.objects.create_user(
    email='faris@company.com',
    username='faris',
    password='123456',
    role='employee'
)
faris.department = 'Engineering'
faris.clearance_level = 1
faris.location = 'Remote'
faris.employee_type = 'fulltime'
faris.save()
print(f"✅ Faris (ACL Employee): faris@company.com / 123456")

# ========== ADDITIONAL EMPLOYEES ==========
print("\n📌 Creating Additional Employees...")

employees = [
    {'email': 'john@company.com', 'username': 'john', 'dept': 'Engineering', 'clearance': 1, 'location': 'Remote'},
    {'email': 'sarah@company.com', 'username': 'sarah', 'dept': 'Marketing', 'clearance': 2, 'location': 'Office'},
    {'email': 'mike@company.com', 'username': 'mike', 'dept': 'IT', 'clearance': 2, 'location': 'Office'},
    {'email': 'emma@company.com', 'username': 'emma', 'dept': 'Finance', 'clearance': 3, 'location': 'Office'},
    {'email': 'david@company.com', 'username': 'david', 'dept': 'HR', 'clearance': 1, 'location': 'Remote'},
    {'email': 'lisa@company.com', 'username': 'lisa', 'dept': 'Engineering', 'clearance': 2, 'location': 'Office'},
]

for emp in employees:
    user = CustomUser.objects.create_user(
        email=emp['email'],
        username=emp['username'],
        password='emp123',
        role='employee'
    )
    user.department = emp['dept']
    user.clearance_level = emp['clearance']
    user.location = emp['location']
    user.employee_type = 'fulltime'
    user.save()
    print(f"✅ {emp['username']} created: {emp['email']} / emp123")

# ========== SAMPLE DOCUMENTS (ABAC) ==========
print("\n📌 Creating Sample Documents for ABAC...")

docs_data = [
    {'title': 'IT Security Policy', 'dept': 'IT', 'clearance': 3, 'content': 'This document contains IT security policies.'},
    {'title': 'HR Employee Handbook', 'dept': 'HR', 'clearance': 2, 'content': 'Employee handbook with HR policies.'},
    {'title': 'Engineering Guidelines', 'dept': 'Engineering', 'clearance': 1, 'content': 'Software engineering best practices.'},
    {'title': 'Financial Report Q4', 'dept': 'Finance', 'clearance': 3, 'content': 'Quarterly financial report.'},
    {'title': 'Marketing Strategy 2025', 'dept': 'Marketing', 'clearance': 2, 'content': 'Marketing strategy and campaign plans.'},
    {'title': 'IT System Architecture', 'dept': 'IT', 'clearance': 2, 'content': 'System architecture design.'},
    {'title': 'Recruitment Plan', 'dept': 'HR', 'clearance': 1, 'content': 'Recruitment and hiring strategy.'},
    {'title': 'Engineering Roadmap', 'dept': 'Engineering', 'clearance': 2, 'content': 'Product development roadmap.'},
    {'title': 'Sales Strategy', 'dept': 'Marketing', 'clearance': 1, 'content': 'Sales strategy and targets.'},
    {'title': 'Executive Summary', 'dept': 'Finance', 'clearance': 3, 'content': 'Executive summary for board.'},
]

for doc_data in docs_data:
    doc = Document.objects.create(
        title=doc_data['title'],
        content=doc_data['content'],
        department=doc_data['dept'],
        clearance_required=doc_data['clearance'],
        created_by=umer
    )
    print(f"✅ Document created: {doc.title}")

# ========== SUMMARY ==========
print("\n" + "=" * 60)
print("✅ ALL USERS AND DOCUMENTS CREATED SUCCESSFULLY!")
print("=" * 60)

print("\n📋 RBAC Users (Role-Based):")
print("  🔵 Admin    : admin@test.com / admin123")
print("  🟡 HR       : hr@test.com / hr123")
print("  🟢 Employee : employee@test.com / emp123")

print("\n📋 ACL Users (User-Specific):")
print("  🔴 Umer  (Full)  : umer@company.com / 123456")
print("  🟡 Salar (HR)    : salar@company.com / 123456")
print("  🟢 Faris (Employee): faris@company.com / 123456")

print("\n📋 Additional Employees:")
print("  👤 john@company.com / emp123")
print("  👤 sarah@company.com / emp123")
print("  👤 mike@company.com / emp123")
print("  👤 emma@company.com / emp123")
print("  👤 david@company.com / emp123")
print("  👤 lisa@company.com / emp123")

print("\n📋 ABAC Attributes:")
for user in CustomUser.objects.all():
    if user.role == 'employee':
        print(f"  {user.email} - Dept: {user.department}, Clearance: {user.clearance_level}, Location: {user.location}")

print("\n📋 Sample Documents (ABAC):")
for doc in Document.objects.all():
    print(f"  {doc.title} - Dept: {doc.department}, Clearance: {doc.clearance_required}")

print("\n" + "=" * 60)
print("🚀 System ready for testing!")
print("=" * 60)