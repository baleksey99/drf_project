from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from .models import Course, Lesson, Subscription
from .serializers import LessonSerializer, SubscriptionSerializer
import re
from datetime import timedelta

User = get_user_model()

class LessonAndSubscriptionTests(APITestCase):
    """Тесты для уроков и подписок на курсы."""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass'
        )
        self.course = Course.objects.create(
            name='Тестовый курс',
            author=self.user
        )
        self.lesson = Lesson.objects.create(
            name='Первый урок',
            course=self.course,
            video_url='https://www.youtube.com/watch?v=test',
            duration=timedelta(minutes=30),
            author=self.user
        )

    def tearDown(self):
        """Очистка после каждого теста."""
        self.client.logout()

    # --- Тесты для уроков ---

    def test_create_lesson_as_author(self):
        """Проверка создания урока автором курса."""
        self.client.force_authenticate(user=self.user)
        data = {
            'name': 'Второй урок',
            'description': 'Продолжение',
            'course': self.course.id,
            'video_url': 'https://youtube.com/watch?v=dQw4w9WgXcQ',
            'duration': '00:30:00'
        }
        response = self.client.post('/api/lessons/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_valid_youtube_links(self):
        """Проверка валидных YouTube‑ссылок через API."""
        self.client.force_authenticate(user=self.user)
        valid_links = [
            'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            'http://youtu.be/dQw4w9WgXcQ',
            'https://www.youtube.com/embed/dQw4w9WgXcQ'
        ]
        for link in valid_links:
            data = {
                'name': f'Урок с валидной ссылкой {link}',
                'course': self.course.id,
                'video_url': link,
                'duration': '00:30:00'
            }
            response = self.client.post('/api/lessons/', data, format='json')
            self.assertEqual(
                response.status_code,
                status.HTTP_201_CREATED,
                f'Ошибка для валидной ссылки: {link} — статус {response.status_code}, ответ: {response.data}'
            )


    def test_cannot_subscribe_twice(self):
        """Проверка запрета повторной подписки."""
        Subscription.objects.create(user=self.user, course=self.course)
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            f'/api/courses/{self.course.id}/subscribe/',
            format='json'
        )
        self.assertIn(
            response.status_code,
            [status.HTTP_400_BAD_REQUEST, status.HTTP_409_CONFLICT]
        )

    def test_subscription_status_in_course_detail(self):
        """Проверка статуса подписки в детализации курса."""
        Subscription.objects.create(user=self.user, course=self.course)
        self.client.force_authenticate(user=self.user)
        response = self.client.get(f'/api/courses/{self.course.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['is_subscribed'])

    # --- Тесты для подписок ---

    def test_subscribe_to_course(self):
        """Проверка подписки на курс."""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            f'/api/courses/{self.course.id}/subscribe/',
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Subscription.objects.filter(
                user=self.user,
                course=self.course
            ).exists()
        )

    def test_unsubscribe_from_course(self):
        """Проверка отписки от курса."""
        Subscription.objects.create(user=self.user, course=self.course)
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(
            f'/api/courses/{self.course.id}/unsubscribe/',
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Subscription.objects.filter(
                user=self.user,
                course=self.course
            ).exists()
        )
