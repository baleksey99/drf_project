from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

# Роутер для CourseViewSet
router = DefaultRouter()
router.register(r'courses', views.CourseViewSet, basename='course')

urlpatterns = [
    path('lessons/', views.LessonList.as_view(), name='lesson-list'),
    path('lessons/<int:pk>/', views.LessonDetail.as_view(), name='lesson-detail'),
    path('lessons/create/', views.LessonCreate.as_view(), name='lesson-create'),
    path('lessons/<int:pk>/update/', views.LessonUpdate.as_view(), name='lesson-update'),
    path('lessons/<int:pk>/delete/', views.LessonDelete.as_view(), name='lesson-delete'),
] + router.urls