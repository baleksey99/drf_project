from .models import Course, Lesson, Subscription
from .validators import validate_youtube_link
from rest_framework import serializers
from datetime import timedelta
import re

class LessonShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'name', 'order', 'duration']
        read_only_fields = ['id', 'order']

class CourseSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Subscription.objects.filter(
                user=request.user,
                course=obj
            ).exists()
        return False

    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'is_subscribed']
        read_only_fields = ['id']

class SubscriptionSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())

    class Meta:
        model = Subscription
        fields = ['user', 'course']

class LessonSerializer(serializers.ModelSerializer):
    course_name = serializers.SerializerMethodField()
    video_url = serializers.URLField(required=False, allow_blank=True)
    duration = serializers.CharField()  # принимаем строку

    def get_course_name(self, obj):
        return obj.course.name

    def validate_duration(self, value):
        """Преобразует строку 'HH:MM:SS' в timedelta."""
        if not value:
            return value

        pattern = r'^(\d{1,2}):(\d{2})(?::(\d{2}))?$'
        match = re.match(pattern, value)
        if not match:
            raise serializers.ValidationError(
                'Формат длительности должен быть HH:MM:SS, HH:MM или MM:SS'
            )

        hours, minutes, seconds = 0, 0, 0
        parts = [int(part) for part in match.groups() if part is not None]

        if len(parts) == 3:
            hours, minutes, seconds = parts
        elif len(parts) == 2:
            minutes, seconds = parts

        if minutes >= 60 or seconds >= 60:
            raise serializers.ValidationError('Минуты и секунды должны быть < 60')

        return timedelta(hours=hours, minutes=minutes, seconds=seconds)

    def validate(self, data):
        video_url = data.get('video_url')
        if video_url:
            try:
                validate_youtube_link(video_url)
            except serializers.ValidationError as e:
                raise serializers.ValidationError({
                    'video_url': str(e)
                })
        return data

    class Meta:
        model = Lesson
        fields = [
            'id', 'name', 'description', 'preview', 'video_url',
            'course', 'author', 'course_name', 'order', 'duration'
        ]
        read_only_fields = ['id', 'author', 'course_name']
