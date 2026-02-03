
from django.db import models
from django.conf import settings
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


class Course(models.Model):
    name = models.CharField(max_length=200)
    preview = models.ImageField(upload_to='course_previews/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='courses'
    )


    stripe_product_id = models.CharField(max_length=100, blank=True, null=True)
    stripe_price_id = models.CharField(max_length=100, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

    CURRENCIES = ['usd', 'eur', 'rub']

    def create_stripe_price(self):
        if self.currency not in self.CURRENCIES:
            raise ValueError(f"Неподдерживаемая валюта: {self.currency}")
        """Создаёт продукт в Stripe через сервис."""
        product = create_product(
            name=self.name,
            description=self.description or "Курс без описания"
        )
        self.stripe_product_id = product.id

    def create_stripe_price(self):
        """Создаёт цену в Stripe через сервис."""
        price_in_cents = int(self.price * 100)
        price = create_price(
            product_id=self.stripe_product_id,
            unit_amount=price_in_cents,
            currency='usd'
        )
        self.stripe_price_id = price.id

    def save(self, *args, **kwargs):
        if not self.stripe_product_id:
            self.create_stripe_product()


        if self.stripe_price_id:
            existing_price = stripe.Price.retrieve(self.stripe_price_id)
            current_price_cents = int(self.price * 100)
            if existing_price.unit_amount != current_price_cents:
                self.create_stripe_price()
        else:
            self.create_stripe_price()

        super().save(*args, **kwargs)

class Subscription(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='subscriptions'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='subscribers'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')

        indexes = [
            models.Index(fields=['user', 'course']),
        ]

    def __str__(self):
        return f"{self.user.username} → {self.course.name}"

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    preview = models.ImageField(upload_to='lesson_previews/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='lessons'
    )
    order = models.PositiveIntegerField(default=1)
    duration = models.DurationField(null=True, blank=True)

    def __str__(self):
        return self.name
