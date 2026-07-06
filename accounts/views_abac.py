from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.db.models import Q
from datetime import datetime
from .models import CustomUser, Document
from .serializers import UserSerializer, LoginSerializer, DocumentSerializer
from .permissions import (
    DepartmentAccess, ClearanceLevelAccess, TimeBasedAccess,
    LocationBasedAccess, EmployeeTypeAccess, CombinedABAC
)

def get_tokens(user):
    refresh = RefreshToken.for_user(user)
    return {'access': str(refresh.access_token), 'refresh': str(refresh)}

@api_view(['POST'])
@permission_classes([AllowAny])
def abac_login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = authenticate(
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )
        if user:
            tokens = get_tokens(user)
            return Response({
                'user': UserSerializer(user).data,
                'tokens': tokens,
                'auth_type': 'ABAC',
                'message': f'Logged in with attributes: Dept={user.department}, Clearance={user.clearance_level}'
            })
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# ===== USER ATTRIBUTES ENDPOINT =====

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def abac_user_attributes(request):
    """Get current user's attributes for ABAC"""
    user = request.user
    return Response({
        'email': user.email,
        'username': user.username,
        'role': user.role,
        'department': user.department,
        'clearance_level': user.clearance_level,
        'location': user.location,
        'employee_type': user.employee_type,
        'is_super_admin': user.is_super_admin
    })

# ===== ABAC ENDPOINTS =====

@api_view(['GET'])
@permission_classes([IsAuthenticated, DepartmentAccess])
def abac_department_documents(request):
    """ABAC: Users can only view documents in their department"""
    documents = Document.objects.filter(department=request.user.department)
    return Response({
        'auth_type': 'ABAC',
        'user_department': request.user.department,
        'total': documents.count(),
        'documents': DocumentSerializer(documents, many=True).data
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated, ClearanceLevelAccess])
def abac_clearance_documents(request, doc_id):
    """ABAC: Users need sufficient clearance level"""
    try:
        doc = Document.objects.get(id=doc_id)
        return Response({
            'auth_type': 'ABAC',
            'user_clearance': request.user.clearance_level,
            'required_clearance': doc.clearance_required,
            'has_access': request.user.clearance_level >= doc.clearance_required,
            'document': DocumentSerializer(doc).data
        })
    except Document.DoesNotExist:
        return Response({'error': 'Document not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated, TimeBasedAccess])
def abac_secure_resource(request):
    """ABAC: Time-based access (9 AM - 6 PM)"""
    current_hour = datetime.now().hour
    return Response({
        'auth_type': 'ABAC',
        'message': 'Access granted based on time',
        'time': 'Working hours (9 AM - 6 PM)',
        'current_hour': current_hour,
        'access_granted': 9 <= current_hour <= 18,
        'data': 'This is sensitive data only available during work hours'
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated, LocationBasedAccess])
def abac_office_resource(request):
    """ABAC: Location-based access (Office only)"""
    return Response({
        'auth_type': 'ABAC',
        'user_location': request.user.location,
        'message': 'This resource is only available for office employees',
        'access_granted': request.user.location == 'Office',
        'data': 'Office-only confidential content'
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated, EmployeeTypeAccess])
def abac_fulltime_resource(request):
    """ABAC: Full-time employees only"""
    return Response({
        'auth_type': 'ABAC',
        'user_type': request.user.employee_type,
        'message': 'This resource is only for full-time employees',
        'access_granted': request.user.employee_type == 'fulltime',
        'data': 'Full-time employee benefits and resources'
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated, CombinedABAC])
def abac_premium_resource(request):
    """ABAC: Multiple attributes required"""
    return Response({
        'auth_type': 'ABAC',
        'message': 'Access granted based on multiple attributes',
        'requirements': [
            'Clearance level >= 2',
            'Office location',
            'Full-time employee'
        ],
        'user_attributes': {
            'clearance_level': request.user.clearance_level,
            'location': request.user.location,
            'employee_type': request.user.employee_type
        },
        'access_granted': (
            request.user.clearance_level >= 2 and
            request.user.location == 'Office' and
            request.user.employee_type == 'fulltime'
        ),
        'data': 'Premium content for senior full-time office employees'
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def abac_create_document(request):
    """Create a document for ABAC testing"""
    data = request.data
    doc = Document.objects.create(
        title=data.get('title', 'Untitled'),
        content=data.get('content', ''),
        department=data.get('department', request.user.department),
        clearance_required=data.get('clearance_required', 1),
        is_confidential=data.get('is_confidential', False),
        created_by=request.user
    )
    return Response({
        'auth_type': 'ABAC',
        'message': 'Document created',
        'document': DocumentSerializer(doc).data
    }, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def abac_all_documents(request):
    """Get all documents (for testing)"""
    documents = Document.objects.all()
    return Response({
        'total': documents.count(),
        'documents': DocumentSerializer(documents, many=True).data
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def abac_create_sample_documents(request):
    """Create sample documents for ABAC testing"""
    # Sample documents for different departments
    docs_data = [
        {
            'title': 'IT Security Policy',
            'content': 'This document contains IT security policies and procedures.',
            'department': 'IT',
            'clearance_required': 3,
            'is_confidential': True
        },
        {
            'title': 'HR Employee Handbook',
            'content': 'Employee handbook with HR policies.',
            'department': 'HR',
            'clearance_required': 2,
            'is_confidential': False
        },
        {
            'title': 'Engineering Guidelines',
            'content': 'Software engineering best practices and guidelines.',
            'department': 'Engineering',
            'clearance_required': 1,
            'is_confidential': False
        },
        {
            'title': 'Financial Report Q4',
            'content': 'Quarterly financial report for Q4 2024.',
            'department': 'Finance',
            'clearance_required': 3,
            'is_confidential': True
        },
        {
            'title': 'Marketing Strategy 2025',
            'content': 'Marketing strategy and campaign plans for 2025.',
            'department': 'Marketing',
            'clearance_required': 2,
            'is_confidential': True
        },
        {
            'title': 'IT System Architecture',
            'content': 'System architecture and infrastructure design.',
            'department': 'IT',
            'clearance_required': 2,
            'is_confidential': True
        },
        {
            'title': 'HR Recruitment Plan',
            'content': 'Recruitment plan and hiring strategy.',
            'department': 'HR',
            'clearance_required': 1,
            'is_confidential': False
        },
        {
            'title': 'Engineering Roadmap',
            'content': 'Product development roadmap and milestones.',
            'department': 'Engineering',
            'clearance_required': 2,
            'is_confidential': True
        },
    ]
    
    created = 0
    for doc_data in docs_data:
        doc, created_status = Document.objects.get_or_create(
            title=doc_data['title'],
            defaults={
                'content': doc_data['content'],
                'department': doc_data['department'],
                'clearance_required': doc_data['clearance_required'],
                'is_confidential': doc_data['is_confidential'],
                'created_by': request.user
            }
        )
        if created_status:
            created += 1
    
    return Response({
        'message': f'Created {created} sample documents',
        'total_documents': Document.objects.count()
    })