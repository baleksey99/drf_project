from rest_framework import generics, viewsets, status, permissions
from django_filters import rest_framework as filters
from .filters import CourseFilter
from .permissions import IsOwnerOrModerator
from rest_framework.response import Response
from rest_framework.decorators import action
from .paginators import StandardResultsSetPagination
from .models import Course, Subscription, Lesson
from .serializers import CourseSerializer, SubscriptionSerializer, LessonSerializer
from materials.tasks import send_course_update_notification

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = CourseFilter
    pagination_class = StandardResultsSetPagination

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwnerOrModerator()]
        elif self.action == 'create':
            return [permissions.IsAuthenticated()]
        else:
            return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Отправляем уведомление после обновления курса
        send_course_update_notification.delay(instance.id)

        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Отправляем уведомление после частичного обновления курса
        send_course_update_notification.delay(instance.id)

        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='subscribe')
    def subscribe(self, request, pk=None):
        """Подписка на курс."""
        course = self.get_object()

        # Проверяем, есть ли уже подписка
        if Subscription.objects.filter(user=request.user, course=course).exists():
            return Response(
                {'error': 'Вы уже подписаны на этот курс'},
                status=status.HTTP_409_CONFLICT
            )

        # Создаём новую подписку
        subscription = Subscription.objects.create(
            user=request.user,
            course=course
        )
        serializer = SubscriptionSerializer(subscription)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['delete'], url_path='unsubscribe')
    def unsubscribe(self, request, pk=None):
        """Отмена подписки на курс."""
        course = self.get_object()
        try:
            subscription = Subscription.objects.get(user=request.user, course=course)
            subscription.delete()
            return Response(
                {'message': 'Подписка отменена'},
                status=status.HTTP_204_NO_CONTENT
            )
        except Subscription.DoesNotExist:
            return Response(
                {'error': 'Подписка не найдена'},
                status=status.HTTP_404_NOT_FOUND
            )

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all().order_by('order')
    serializer_class = LessonSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.DjangoFilterBackend]

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwnerOrModerator()]
        elif self.action == 'create':
            return [permissions.IsAuthenticated()]
        else:
            return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
