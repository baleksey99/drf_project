
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet


router = DefaultRouter()
router.register(r'courses', CourseViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('courses/', views.CourseList.as_view(), name='course-list'),
    path('courses/<int:pk>/', views.CourseDetail.as_view(), name='course-detail'),
    path('lessons/', views.LessonList.as_view(), name='lesson-list'),
    path('lessons/<int:pk>/', views.LessonDetail.as_view(), name='lesson-detail'),
]