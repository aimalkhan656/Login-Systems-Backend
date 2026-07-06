from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'

class IsHR(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'hr'

class IsEmployee(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'employee'

class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'manager'

class IsAdminOrHR(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['admin', 'hr']

class IsUmer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.email == 'umer@company.com'

class IsSalar(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.email == 'salar@company.com'

class IsFaris(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.email == 'faris@company.com'

class IsSpecificEmployee(permissions.BasePermission):
    allowed_emails = ['umer@company.com', 'salar@company.com', 'mike@company.com']
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.email in self.allowed_emails

# ABAC Permissions
class DepartmentAccess(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return True
        return obj.department == request.user.department

class ClearanceLevelAccess(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        return request.user.clearance_level >= obj.clearance_required

class TimeBasedAccess(permissions.BasePermission):
    def has_permission(self, request, view):
        from datetime import datetime
        if not request.user.is_authenticated:
            return False
        if request.user.role == 'admin':
            return True
        current_hour = datetime.now().hour
        return 9 <= current_hour <= 18

class LocationBasedAccess(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.location == 'Office'

class EmployeeTypeAccess(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.employee_type == 'fulltime'

class CombinedABAC(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return (
            request.user.clearance_level >= 2 and
            request.user.location == 'Office' and
            request.user.employee_type == 'fulltime'
        )