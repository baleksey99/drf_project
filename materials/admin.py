from django.contrib import admin
from .models import Course, Lesson, Subscription


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'author')
    search_fields = ('name', 'description')
    list_filter = ('author',)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('name', 'course', 'author', 'order')
    search_fields = ('name',)
    list_filter = ('course', 'author')

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'created_at')
    list_filter = ('created_at', 'course')
    search_fields = ('user__username', 'course__name')
