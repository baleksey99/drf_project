from celery import shared_task
from django.contrib.auth.models import User
from django.utils import timezone


@shared_task
def check_inactive_users():
    one_month_ago = timezone.now() - timezone.timedelta(days=30)

    inactive_users = User.objects.filter(
        last_login__lt=one_month_ago,
        is_active=True
    )

    for user in inactive_users:
        user.is_active = False
        user.save(update_fields=['is_active'])

    return f'Заблокировано пользователей: {inactive_users.count()}'


@shared_task
def block_inactive_users():
    inactive_users = User.objects.filter(is_active=False)
    for user in inactive_users:
        user.is_active = False
        user.save()