from rest_framework import generics, viewsets, status, permissions
from django_filters import rest_framework as filters
from .filters import CourseFilter
from .permissions import IsOwnerOrModerator
from rest_framework.response import Response
from rest_framework.decorators import action
from .paginators import StandardResultsSetPagination
from .models import Course, Subscription, Lesson
from .serializers import CourseSerializer, SubscriptionSerializer, LessonSerializer



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

    @action(detail=True, methods=['post'], url_path='subscribe')
    def subscribe(self, request, pk=None):
        """Подписка на курс."""
        course = self.get_object()
        subscription, created = Subscription.objects.get_or_create(
            user=request.user,
            course=course
        )
        if created:
            serializer = SubscriptionSerializer(subscription)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'message': 'Вы уже подписаны'}, status=status.HTTP_200_OK)

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
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = StandardResultsSetPagination

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwnerOrModerator()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        course = serializer.validated_data['course']
        if course.author != self.request.user:
            raise PermissionDenied("Вы не можете создавать уроки для чужого курса")
        serializer.save(author=self.request.user)
