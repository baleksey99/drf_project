from celery import shared_task
from django.core.mail import send_mail
from .models import Course, Subscription  # + импорт Subscription
import logging

logger = logging.getLogger(__name__)


@shared_task
def send_course_update_notification(course_id):
    try:
        course = Course.objects.get(id=course_id)
        subscriptions = Subscription.objects.filter(course=course)  # Получаем всех подписчиков

        for subscription in subscriptions:
            subject = f'Обновление курса: {course.name}'
            message = f'Курс "{course.name}" был обновлён. Заходите и изучайте новые материалы!'
            send_mail(
                subject,
                message,
                'from@example.com',
                [subscription.user.email],  # Отправляем каждому подписчику
                fail_silently=False,
            )
            logger.info(f'Уведомление отправлено пользователю {subscription.user.email} для курса {course.name}')

        return f'Уведомления об обновлении курса "{course.name}" отправлены {len(subscriptions)} подписчикам.'

    except Course.DoesNotExist:
        logger.error(f'Курс с ID {course_id} не найден')
        return 'Курс не найден.'
    except Exception as e:
        logger.error(f'Ошибка при отправке уведомлений: {str(e)}')
        return f'Ошибка при отправке уведомления: {str(e)}'
