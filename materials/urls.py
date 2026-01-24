
from django.urls import path
from . import views

urlpatterns = [
    path('courses/', views.CourseList.as_view(), name='course-list'),
    path('courses/<int:pk>/', views.CourseDetail.as_view(), name='course-detail'),
    path('lessons/', views.LessonList.as_view(), name='lesson-list'),
    path('lessons/<int:pk>/', views.LessonDetail.as_view(), name='lesson-detail'),
]