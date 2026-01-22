from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def api_root(request):
    return HttpResponse("Добро пожаловать в API LMS!", status=200)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api_root),  # Обработчик для /api/
    path('api/', include('materials.urls')),  # Вложенные URL
]