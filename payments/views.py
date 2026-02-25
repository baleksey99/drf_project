from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from .services import create_product, create_price, create_checkout_session


class CreateProductView(View):
    """
    API-эндпоинт для создания продукта и цены в Stripe.
    Пример запроса: POST /api/create-product/
    """
<<<<<<< HEAD

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
=======
    def post(self, request):
        try:
           
            course_id = request.POST.get('course_id') 

            # 2. Получаем объект курса из БД
            course = Course.objects.get(id=course_id)

            product = create_product(
                name=course.name, 
                description=course.description  
            )

            
            price = create_price(
                product_id=product.id,
                unit_amount=10000,  # $100.00 (можно также сделать динамическим)
>>>>>>> 4aa57d4b33958df394a638c916e2f61778f6d1c9
                currency='usd'
            )

            return JsonResponse({
                'product_id': product.id,
                'price_id': price.id,
                'message': 'Продукт и цена созданы'
            })
<<<<<<< HEAD
=======
        except Course.DoesNotExist:
            return JsonResponse({'error': 'Курс не найден'}, status=404)
>>>>>>> 4aa57d4b33958df394a638c916e2f61778f6d1c9
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


<<<<<<< HEAD
=======

>>>>>>> 4aa57d4b33958df394a638c916e2f61778f6d1c9
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
