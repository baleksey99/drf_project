from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from .services import create_product, create_price, create_checkout_session


class CreateProductView(View):
    """
    API-эндпоинт для создания продукта и цены в Stripe.
    Пример запроса: POST /api/create-product/
    """

    def post(self, request):
        try:
            # 1. Создаём продукт
            product = create_product(
                name="Курс по Django",
                description="Изучите Django за 30 дней"
            )

            # 2. Создаём цену
            price = create_price(
                product_id=product.id,
                unit_amount=10000,  # $100.00
                currency='usd'
            )

            return JsonResponse({
                'product_id': product.id,
                'price_id': price.id,
                'message': 'Продукт и цена созданы'
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class CheckoutView(View):
    """
    Отображает кнопку для перехода на страницу оплаты Stripe.
    Пример: GET /checkout/<price_id>/
    """

    def get(self, request, price_id):
        try:
            session = create_checkout_session(
                price_id=price_id,
                success_url="http://localhost:8000/success/",
                cancel_url="http://localhost:8000/cancel/"
            )

            return render(request, 'payments/checkout.html', {
                'session_id': session.id,
                'publishable_key': settings.STRIPE_PUBLISHABLE_KEY
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
