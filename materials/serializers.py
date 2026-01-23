from rest_framework import serializers
from .models import Course, Lesson
from users.models import Payment


class CourseSerializer(serializers.ModelSerializer):
    # Добавляем поле для подсчёта уроков
    number_of_lessons = serializers.SerializerMethodField()

    class Meta:
        model = Course
        # Включаем новое поле в список выводимых полей
        fields = '__all__'  # или явно: ['id', 'name', 'preview', 'description', 'number_of_lessons']

    def get_number_of_lessons(self, obj):
        """
        Метод для вычисления значения поля number_of_lessons.
        obj — экземпляр модели Course.
        """
        return obj.lessons.count()  # Используем related_name='lessons' из модели Lesson

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'



class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'