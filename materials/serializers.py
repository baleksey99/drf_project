from .models import Course, Lesson, Subscription
from .validators import YouTubeLinkValidator
from rest_framework import serializers

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
    course_name = serializers.SerializerMethodField()  # ← Добавлено
    video_url = serializers.URLField(required=False)

    def get_course_name(self, obj):  # ← Реализовано
        return obj.course.name

    class Meta:
        model = Lesson
        fields = [
            'id', 'name', 'description', 'preview', 'video_url',
            'course', 'author', 'course_name', 'order', 'duration'
        ]
        read_only_fields = ['id', 'author', 'course_name']
        validators = [YouTubeLinkValidator(field='video_url')]
