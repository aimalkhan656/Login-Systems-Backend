from django.urls import path
from . import views_rbac, views_acl, views_abac

urlpatterns = [
    # ===== RBAC URLs =====
    path('rbac/login/', views_rbac.rbac_login, name='rbac-login'),
    path('rbac/admin/', views_rbac.rbac_admin_dashboard, name='rbac-admin'),
    path('rbac/hr/', views_rbac.rbac_hr_dashboard, name='rbac-hr'),
    path('rbac/employee/', views_rbac.rbac_employee_dashboard, name='rbac-employee'),
    path('rbac/manager/', views_rbac.rbac_manager_dashboard, name='rbac-manager'),
    path('rbac/admin-hr/', views_rbac.rbac_admin_hr_dashboard, name='rbac-admin-hr'),
    
    # ===== ACL URLs =====
    path('acl/login/', views_acl.acl_login, name='acl-login'),
    path('acl/umer/', views_acl.acl_umer_dashboard, name='acl-umer'),
    path('acl/salar/', views_acl.acl_salar_dashboard, name='acl-salar'),
    path('acl/faris/', views_acl.acl_faris_dashboard, name='acl-faris'),
    path('acl/employees/', views_acl.acl_employee_list, name='acl-employees'),
    path('acl/delete/<int:user_id>/', views_acl.acl_delete_user, name='acl-delete'),
    
    # ===== ABAC URLs =====
    path('abac/login/', views_abac.abac_login, name='abac-login'),
    path('abac/user-attributes/', views_abac.abac_user_attributes, name='abac-user-attributes'),
    path('abac/documents/', views_abac.abac_department_documents, name='abac-documents'),
    path('abac/all-documents/', views_abac.abac_all_documents, name='abac-all-documents'),
    path('abac/document/<int:doc_id>/', views_abac.abac_clearance_documents, name='abac-clearance'),
    path('abac/secure/', views_abac.abac_secure_resource, name='abac-secure'),
    path('abac/office/', views_abac.abac_office_resource, name='abac-office'),
    path('abac/fulltime/', views_abac.abac_fulltime_resource, name='abac-fulltime'),
    path('abac/premium/', views_abac.abac_premium_resource, name='abac-premium'),
    path('abac/create-document/', views_abac.abac_create_document, name='abac-create-document'),
    path('abac/create-sample-docs/', views_abac.abac_create_sample_documents, name='abac-create-sample-docs'),
    
    # ===== Regular Login =====
    path('login/', views_rbac.rbac_login, name='login'),
]