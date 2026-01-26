from rest_framework import serializers
from .models import Course, Lesson




class LessonShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = [
            'id',
            'title',
            'order',
            'duration',
        ]
        read_only_fields = ['id', 'order']



class CourseSerializer(serializers.ModelSerializer):

    number_of_lessons = serializers.SerializerMethodField()
    lessons = LessonShortSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = [
            'id',
            'title',
            'description',
            'start_date',
            'end_date',
            'number_of_lessons',
            'lessons',

        ]
        read_only_fields = ['id']

    def get_number_of_lessons(self, obj):

        return obj.lessons.count()



class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'



