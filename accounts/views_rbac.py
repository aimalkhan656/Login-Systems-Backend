from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import CustomUser
from .serializers import UserSerializer, LoginSerializer
from .permissions import IsAdmin, IsHR, IsEmployee, IsManager, IsAdminOrHR

def get_tokens(user):
    refresh = RefreshToken.for_user(user)
    return {'access': str(refresh.access_token), 'refresh': str(refresh)}

@api_view(['POST'])
@permission_classes([AllowAny])
def rbac_login(request):
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
                'auth_type': 'RBAC',
                'message': f'Logged in as {user.role}'
            })
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@permission_classes([IsAdmin])
def rbac_admin_dashboard(request):
    users = CustomUser.objects.all()
    return Response({
        'auth_type': 'RBAC',
        'role': 'Admin',
        'permissions': ['view_all', 'add', 'edit', 'delete'],
        'users': UserSerializer(users, many=True).data
    })

@api_view(['GET'])
@permission_classes([IsHR])
def rbac_hr_dashboard(request):
    employees = CustomUser.objects.filter(role='employee')
    return Response({
        'auth_type': 'RBAC',
        'role': 'HR',
        'permissions': ['view_employees', 'add_employees'],
        'employees': UserSerializer(employees, many=True).data
    })

@api_view(['GET'])
@permission_classes([IsEmployee])
def rbac_employee_dashboard(request):
    return Response({
        'auth_type': 'RBAC',
        'role': 'Employee',
        'permissions': ['view_own_profile'],
        'profile': UserSerializer(request.user).data
    })

@api_view(['GET'])
@permission_classes([IsManager])
def rbac_manager_dashboard(request):
    return Response({
        'auth_type': 'RBAC',
        'role': 'Manager',
        'permissions': ['view_team', 'approve_requests'],
        'team': UserSerializer(CustomUser.objects.filter(department=request.user.department), many=True).data
    })

@api_view(['GET'])
@permission_classes([IsAdminOrHR])
def rbac_admin_hr_dashboard(request):
    return Response({
        'auth_type': 'RBAC',
        'role': request.user.role,
        'message': 'Access granted for Admin or HR'
    })