from rest_framework import serializers
from .models import Course, Lesson
from users.models import Payment


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'name', 'content', 'order']  # добавьте нужные поля

class CourseSerializer(serializers.ModelSerializer):
    number_of_lessons = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)  # вложенные уроки

    class Meta:
        model = Course
        fields = [
            'id',
            'name',
            'description',
            'created_at',
            'number_of_lessons',
            'lessons'
        ]

    def get_number_of_lessons(self, obj):
        return obj.lessons.count()

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'