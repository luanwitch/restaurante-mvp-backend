from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

# Create your views here.
@api_view(['GET']) 
@permission_classes([IsAuthenticated]) 
def me(request):
    user = request.user

    return Response({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'is_staff': user.is_staff,
        'is_superuser': user.is_superuser,
    })