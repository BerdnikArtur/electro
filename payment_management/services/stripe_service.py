import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_payment_intent(amount, currency='usd'):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    
    intent = stripe.PaymentIntent.create(
        amount=int(amount * 100),  # Amount in cents
        currency=currency,
        payment_method_types=['card']
    )
    return intent