from django.urls import path, re_path
from django.conf.urls.static import static
from django.conf import settings

from .views import *

urlpatterns = [
    path('home/checkout/', CheckoutPage.as_view(), name='checkout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)