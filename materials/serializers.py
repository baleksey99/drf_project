from rest_framework import serializers
from .models import Course, Lesson

class LessonShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = [
            'id',
            'name',
            'order',
            'duration',
        ]
        read_only_fields = ['id', 'order']


class CourseSerializer(serializers.ModelSerializer):
    number_of_lessons = serializers.SerializerMethodField()
    lessons = LessonShortSerializer(many=True, read_only=True)
    author = serializers.ReadOnlyField(source='author.username')  # Добавляем автора

    class Meta:
        model = Course
        fields = [
            'id',
            'name',
            'description',
            'start_date',
            'end_date',
            'number_of_lessons',
            'lessons',
            'author',
            'preview',
        ]
        read_only_fields = ['id', 'author', 'preview']

    def get_number_of_lessons(self, obj):
        return obj.lessons.count()

class LessonSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    course_name = serializers.ReadOnlyField(source='course.name')

    class Meta:
        model = Lesson
        fields = [
            'id',
            'name',
            'description',
            'preview',
            'video_url',
            'course',
            'author',
            'course_name',
        ]
        read_only_fields = ['id', 'author', 'course_name']
