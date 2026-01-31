from rest_framework import status, permissions, generics, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer
from .permissions import IsOwnerOrModerator, IsModerator
from .models import User

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = serializer.validate(serializer.data)
        if not user.is_active:
            return Response({'error': 'Пользователь неактивен'}, status=status.HTTP_403_FORBIDDEN)

        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    except Exception:
        return Response({'error': 'Неверные учётные данные'}, status=status.HTTP_401_UNAUTHORIZED)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwnerOrModerator]

    def get_permissions(self):
        # Регистрация и список — без авторизации
        if self.action in ['create', 'list']:
            return [permissions.AllowAny()]
        # Остальные действия — проверка владельца или модератора
        return [IsOwnerOrModerator()]

    def get_queryset(self):
        # Модераторы видят всех, обычные пользователи — только себя
        if self.request.user.groups.filter(name='moderators').exists():
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)
