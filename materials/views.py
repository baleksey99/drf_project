from rest_framework import generics, viewsets, status, permissions
from django_filters import rest_framework as filters
from .filters import CourseFilter
from .permissions import IsOwnerOrModerator
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .paginators import StandardResultsSetPagination
from .models import Course, Subscription, Lesson
from .serializers import CourseSerializer, SubscriptionSerializer, LessonSerializer
from rest_framework.exceptions import NotFound, PermissionDenied

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

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def subscribe(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        raise NotFound('Курс не найден')

    if Subscription.objects.filter(user=request.user, course=course).exists():
        return Response(
            {'message': 'Вы уже подписаны на этот курс'},
            status=status.HTTP_200_OK
        )

    subscription = Subscription.objects.create(user=request.user, course=course)
    serializer = SubscriptionSerializer(subscription)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def unsubscribe(request, course_id):
    try:
        subscription = Subscription.objects.get(user=request.user, course_id=course_id)
        subscription.delete()
        return Response(
            {'message': 'Подписка отменена'},
            status=status.HTTP_204_NO_CONTENT
        )
    except Subscription.DoesNotExist:
        raise NotFound('Подписка не найдена')
