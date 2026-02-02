import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_product(name: str, description: str = None):
    """Создаёт продукт в Stripe."""
    return stripe.Product.create(
        name=name,
        description=description
    )

def create_price(product_id: str, unit_amount: int, currency: str = 'usd'):
    """Создаёт цену для продукта."""
    return stripe.Price.create(
        product=product_id,
        unit_amount=unit_amount,
        currency=currency,
        billing_scheme='per_unit'
    )

def create_checkout_session(price_id: str, success_url: str, cancel_url: str):
    """Создаёт сессию Checkout для оплаты."""
    return stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                'price': price_id,
                'quantity': 1,
            },
        ],
        mode='payment',
        success_url=success_url,
        cancel_url=cancel_url,
    )
