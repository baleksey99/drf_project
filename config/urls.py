from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('materials.urls')),      # Маршруты для курсов/уроков
    path('api/', include('users.urls')),          # Маршруты для платежей/пользователей
]
