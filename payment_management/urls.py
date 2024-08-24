from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from .views import *

urlpatterns = [
    path('config/', stripe_config, name='stripe_config'),
    path('payment-intent/', payment_intent, name='payment_intent'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)