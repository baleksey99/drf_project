from celery import shared_task
from django.core.mail import send_mail
from .models import Course


@shared_task
def send_course_update_notification(course_id):
    try:
        course = Course.objects.get(id=course_id)
        subject = f'Обновление курса: {course.name}'
        message = f'Курс "{course.name}" был обновлён. Заходите и изучайте новые материалы!'
        send_mail(
            subject,
            message,
            'from@example.com',
            [course.author.email],
            fail_silently=False,
        )
        return f'Уведомление об обновлении курса "{course.name}" отправлено.'
    except Course.DoesNotExist:
        return 'Курс не найден.'
    except Exception as e:
        return f'Ошибка при отправке уведомления: {str(e)}'