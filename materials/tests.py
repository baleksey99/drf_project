from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from .models import Course, Lesson, Subscription
from .serializers import LessonSerializer, SubscriptionSerializer
import re
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.exceptions import ValidationError

from materials.validators import validate_youtube_link
from materials.models import Course, Lesson, Subscription

User = get_user_model()



class LessonAndSubscriptionTests(APITestCase):
    """Тесты для уроков и подписок на курсы."""

    def setUp(self):
        """Подготовка тестовых данных перед каждым тестом."""
        self.client = APIClient()

        # Создаём двух пользователей для проверки прав доступа
        self.user1 = User.objects.create_user(
            username='user1',
            password='pass123',
            email='user1@example.com'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            password='pass123',
            email='user2@example.com'
        )

        # Создаём курс (автор — user1)
        self.course = Course.objects.create(
            name='Test Course',
            author=self.user1
        )

        # Создаём урок (принадлежит курсу, автор — user1)
        self.lesson = Lesson.objects.create(
            name='Первый урок',
            description='Введение',
            course=self.course,
            author=self.user1,
            order=1,
            duration='00:30:00'  # Формат строки для DurationField
        )

    def tearDown(self):
        """Очистка после каждого теста."""
        self.client.logout()

    # --- Тесты для уроков ---

    def test_create_lesson_as_author(self):
        """Проверка создания урока автором курса."""
        self.client.force_authenticate(user=self.user1)
        data = {
            'name': 'Второй урок',
            'description': 'Продолжение',
            'course': self.course.id,
            'video_url': 'https://youtube.com/watch?v=dQw4w9WgXcQ'
        }
        response = self.client.post('/api/lessons/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_create_lesson_as_other_user(self):
        """Проверка запрета создания урока не-автором."""
        self.client.force_authenticate(user=self.user2)
        data = {
            'name': 'Чужой урок',
            'description': 'Не должен создаться',
            'course': self.course.id,
            'author': self.user2.id
        }
        response = self.client.post('/api/lessons/', data, format='json')
        self.assertIn(
            response.status_code,
            [status.HTTP_400_BAD_REQUEST, status.HTTP_403_FORBIDDEN]
        )

    def test_update_lesson_as_author(self):
        """Проверка обновления урока автором."""
        self.client.force_authenticate(user=self.user1)
        data = {'name': 'Обновлённый урок'}
        response = self.client.patch(
            f'/api/lessons/{self.lesson.id}/',
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.name, 'Обновлённый урок')


    def test_delete_lesson_as_author(self):
        """Проверка удаления урока автором."""
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(f'/api/lessons/{self.lesson.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lesson.objects.filter(id=self.lesson.id).exists())


    def test_list_lessons_as_anonymous(self):
        """Проверка просмотра списка уроков неавторизованным пользователем."""
        self.client.force_authenticate(user=None)
        response = self.client.get('/api/lessons/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 1)


    def test_retrieve_lesson_as_anonymous(self):
        """Проверка просмотра урока неавторизованным пользователем."""
        self.client.force_authenticate(user=None)
        response = self.client.get(f'/api/lessons/{self.lesson.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    # --- Тесты для подписок ---


    def test_subscribe_to_course(self):
        """Проверка подписки на курс."""
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(
            f'/api/courses/{self.course.id}/subscribe/',
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Subscription.objects.filter(
                user=self.user1,
                course=self.course
            ).exists()
        )

    def test_unsubscribe_from_course(self):
        """Проверка отписки от курса."""
        Subscription.objects.create(user=self.user1, course=self.course)
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(
            f'/api/courses/{self.course.id}/unsubscribe/',
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Subscription.objects.filter(
                user=self.user1,
                course=self.course
            ).exists()
        )

    def test_cannot_subscribe_twice(self):
        """Проверка запрета повторной подписки."""
        Subscription.objects.create(user=self.user1, course=self.course)
        self.client.force_authenticate(user=self.user1)
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
        Subscription.objects.create(user=self.user1, course=self.course)
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(f'/api/courses/{self.course.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['is_subscribed'])




    def test_valid_youtube_links(self):
        """Проверка валидных YouTube-ссылок."""
        valid_links = [
            'https://youtube.com/watch?v=dQw4w9WgXcQ',
            'http://youtu.be/dQw4w9WgXcQ',
            'https://www.youtube.com/playlist?list=PL...'
        ]
        for link in valid_links:
            try:
                validate_youtube_link(link)
            except ValidationError:
                self.fail(f'Ссылка {link} должна быть валидной')

    def test_invalid_youtube_links(self):
        """Проверка невалидных YouTube-ссылок."""
        invalid_links = [
            'https://example.com',
            'http://notyoutube.com',
            'just-text',
        ]
        for link in invalid_links:
            with self.assertRaises(ValidationError):
                validate_youtube_link(link)
