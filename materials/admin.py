from django.contrib import admin
from .models import Course, Lesson, Subscription

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'created_at', 'updated_at')  # ← добавлены даты
    search_fields = ('name', 'description')
    list_filter = ('author', 'created_at')  # ← фильтр по дате создания
    readonly_fields = ('created_at', 'updated_at')  # ← если есть такие поля

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('name', 'course', 'author', 'order', 'duration')  # ← добавлено duration
    search_fields = ('name',)
    list_filter = ('course', 'author', 'order')  # ← фильтр по порядку
    ordering = ('course', 'order')  # ← сортировка в админке

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'created_at')
    list_filter = ('created_at', 'course')
    search_fields = ('user__username', 'course__name')
    date_hierarchy = 'created_at'  # ← удобная навигация по датам
