from .models import Course, Lesson, Subscription
from .validators import YouTubeLinkValidator
from rest_framework import serializers
from rest_framework import serializers
from .models import Course
from .tasks import send_course_update_email
from django.utils import timezone


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

        read_only_fields = ['id']  # ← Добавлено для защиты ID


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
    video_url = serializers.URLField(required=False, allow_blank=True)  # ← allow_blank


    def get_course_name(self, obj):
        return obj.course.name


    class Meta:
        model = Lesson
        fields = [
            'id', 'name', 'description', 'preview', 'video_url',
            'course', 'author', 'course_name', 'order', 'duration'
        ]
        read_only_fields = ['id', 'author', 'course_name']
        validators = [YouTubeLinkValidator(field='video_url')]


    def validate(self, data):
        """
        Дополнительная проверка: если video_url указан, он должен быть валидным.
        """
        video_url = data.get('video_url')
        if video_url and video_url.strip():
            validate_youtube_link(video_url)
        return data



class CourseSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        # Проверяем, не обновлялся ли курс за последние 4 часа
        four_hours_ago = timezone.now() - timezone.timedelta(hours=4)
        if instance.updated_at < four_hours_ago:
            # Обновляем поле updated_at
            instance.updated_at = timezone.now()
            # Запускаем задачу на отправку писем
            send_course_update_email.delay(instance.id)

        return super().update(instance, validated_data)
