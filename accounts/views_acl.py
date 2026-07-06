from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import CustomUser
from .serializers import UserSerializer, LoginSerializer
from .permissions import IsUmer, IsSalar, IsFaris, IsSpecificEmployee

def get_tokens(user):
    refresh = RefreshToken.for_user(user)
    return {'access': str(refresh.access_token), 'refresh': str(refresh)}

@api_view(['POST'])
@permission_classes([AllowAny])
def acl_login(request):
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
                'auth_type': 'ACL',
                'message': f'Logged in as {user.email} (ACL specific)'
            })
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@permission_classes([IsUmer])
def acl_umer_dashboard(request):
    users = CustomUser.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response({
        'auth_type': 'ACL',
        'user': 'Umer (specific user)',
        'permissions': ['ALL_PERMISSIONS'],
        'message': 'Only Umer can see this',
        'users': serializer.data
    })

@api_view(['GET'])
@permission_classes([IsSalar])
def acl_salar_dashboard(request):
    employees = CustomUser.objects.filter(role='employee')
    serializer = UserSerializer(employees, many=True)
    return Response({
        'auth_type': 'ACL',
        'user': 'Salar (specific user)',
        'permissions': ['view_employees', 'add_employees'],
        'message': 'Only Salar can see this',
        'employees': serializer.data
    })

@api_view(['GET'])
@permission_classes([IsFaris])
def acl_faris_dashboard(request):
    return Response({
        'auth_type': 'ACL',
        'user': 'Faris (specific user)',
        'permissions': ['view_own_profile'],
        'message': 'Only Faris can see this',
        'profile': UserSerializer(request.user).data
    })

@api_view(['GET'])
@permission_classes([IsSpecificEmployee])
def acl_employee_list(request):
    employees = CustomUser.objects.filter(role='employee')
    return Response({
        'auth_type': 'ACL',
        'message': 'Access granted to specific employees list',
        'allowed_users': ['umer@company.com', 'salar@company.com', 'mike@company.com'],
        'employees': UserSerializer(employees, many=True).data
    })

@api_view(['DELETE'])
@permission_classes([IsUmer])
def acl_delete_user(request, user_id):
    try:
        user = CustomUser.objects.get(id=user_id)
        if user.is_superuser:
            return Response({'error': 'Cannot delete superuser'}, status=status.HTTP_403_FORBIDDEN)
        user.delete()
        return Response({
            'auth_type': 'ACL',
            'message': f'User deleted by Umer (ACL)',
            'deleted_user_id': user_id
        })
    except CustomUser.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)