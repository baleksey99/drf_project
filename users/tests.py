from django.test import TestCase
from rest_framework.test import APITestCase
from materials.models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer


class CourseModelTest(TestCase):
    """Тесты для модели Course"""

    def setUp(self):
        self.course = Course.objects.create(
            name="Тестовый курс",
            description="Описание курса"
        )

    def test_course_creation(self):
        """Проверка создания курса"""
        self.assertEqual(self.course.title, "Тестовый курс")
        self.assertEqual(Course.objects.count(), 1)


class CourseApiTest(APITestCase):
    """Тесты API для курсов"""

    def setUp(self):
        self.course = Course.objects.create(
            name="API Курс",
            description="API Описание"
        )

    def test_get_courses(self):
        """Тест получения списка курсов"""
        response = self.client.get('/api/courses/')
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)
