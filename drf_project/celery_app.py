import os
from celery import Celery
from django.conf import settings

# Настройка: используем переменные окружения
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drf_project.settings')

app = Celery('drf_project')

# Загрузка настроек из Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автообнаружение задач в приложениях
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
