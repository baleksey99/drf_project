from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, LessonViewSet, subscribe, unsubscribe


router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'lessons', LessonViewSet, basename='lesson')


urlpatterns = [
    path('api/', include(router.urls)),  # ← Добавлен префикс /api/


    path(
        'api/courses/<int:course_id>/subscribe/',
        subscribe,
        name='subscribe'
    ),
    path(
        'api/courses/<int:course_id>/unsubscribe/',
        unsubscribe,
        name='unsubscribe'
    ),
]
