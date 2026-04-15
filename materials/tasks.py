from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_course_update_notification(course_id):
    """
    Асинхронная отправка уведомлений подписчикам об обновлении курса.
    """
    # Отложенный импорт моделей — выполняется только при вызове задачи
    from materials.models import Course, Subscription

    try:
        course = Course.objects.get(id=course_id)
        subscriptions = Subscription.objects.filter(course=course)

        sent_count = 0
        failed_count = 0

        for subscription in subscriptions:
            if subscription.user.email:
                subject = f'Обновление курса: {course.name}'
                message = (
                    f'Курс "{course.name}" был обновлён. '
                    'Заходите и изучайте новые материалы!'
                )
                try:
                    send_mail(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL,
                        [subscription.user.email],
                        fail_silently=False,
                    )
                    sent_count += 1
                    logger.info(
                        f'Уведомление отправлено пользователю {subscription.user.email} '
                        f'для курса {course.name}'
                    )
                except Exception as e:
                    failed_count += 1
                    logger.error(
                        f'Ошибка отправки уведомления пользователю '
                        f'{subscription.user.email}: {str(e)}'
                    )

        logger.info(
            f'Уведомления об обновлении курса "{course.name}" отправлены: '
            f'{sent_count} успешно, {failed_count} с ошибками.'
        )
        return (
            f'Уведомления об обновлении курса "{course.name}" '
            f'отправлены {sent_count} подписчикам.'
        )

    except Course.DoesNotExist:
        logger.error(f'Курс с ID {course_id} не найден')
        return 'Курс не найден.'
    except Exception as e:
        logger.error(f'Критическая ошибка при отправке уведомлений: {str(e)}')
        return f'Ошибка при отправке уведомления: {str(e)}'