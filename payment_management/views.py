from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from .models import *
from.services import stripe_service


@csrf_exempt
def stripe_config(request):
    if request.method == "GET" and request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({'publicKey': settings.STRIPE_PUBLISHABLE_KEY})

@csrf_exempt
def payment_intent(request):
    if request.method == 'POST' and request.headers.get("X-Requested-With") == "XMLHttpRequest":
        amount = request.user.cart.total_price
        try:
            intent = stripe_service.create_payment_intent(amount)
            return JsonResponse({'client_secret': intent.client_secret})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

