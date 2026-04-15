from django.test import TestCase
from rest_framework.test import APITestCase
from materials.models import Course, Lesson
from materials.serializers import CourseSerializer, LessonSerializer


class CourseModelTest(TestCase):
    def setUp(self):
        # Создаём пользователя
        self.user = User.objects.create_user(
            username='modeltest',
            password='testpass'
        )

        # Передаём автора при создании курса
        self.course = Course.objects.create(
            name="Тестовый курс",
            description="Описание курса",
            author=self.user  # добавляем автора
        )


class CourseApiTest(TestCase):
    def setUp(self):

        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )


        self.course = Course.objects.create(
            name="API Курс",
            description="API Описание",
            author=self.user  # добавляем автора
        )
