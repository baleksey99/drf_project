from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import Course, Subscription


@shared_task
def send_course_update_email(course_id):
    try:
        course = Course.objects.get(id=course_id)
        subscriptions = Subscription.objects.filter(course=course, is_active=True)

        for subscription in subscriptions:
            context = {
                'user': subscription.user,
                'course': course,
            }
            subject = f'Обновление курса: {course.title}'
            message = render_to_string('emails/course_update.txt', context)

            send_mail(
                subject,
                message,
                'noreply@example.com',
                [subscription.user.email],
                fail_silently=False,
            )
    except Course.DoesNotExist:
        pass
