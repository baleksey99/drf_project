from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name='Город')

    # Переопределяем поля groups и user_permissions с уникальными related_name
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='custom_user_set',
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='custom_user_set',
        related_query_name='user',
    )

class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Наличные'),
        ('transfer', 'Перевод на счёт'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    payment_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата оплаты'
    )
    course = models.ForeignKey(
        'materials.Course',  # Ссылка на модель Course из приложения materials
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Оплаченный курс'
    )
    lesson = models.ForeignKey(
        'materials.Lesson',  # Ссылка на модель Lesson из приложения materials
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Оплаченный урок'
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Сумма оплаты'
    )
    method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        verbose_name='Способ оплаты'
    )

    def __str__(self):
        return f'Оплата {self.amount} от {self.user.username}'

    class Meta:
        verbose_name = 'Платёж'
        verbose_name_plural = 'Платежи'

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.username
