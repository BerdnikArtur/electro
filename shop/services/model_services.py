from django.db.models.manager import BaseManager
from django.db.models import Q
from django.http import HttpRequest
from django.utils.safestring import SafeText
from django.utils import timezone

from shop.models import *

from datetime import timedelta
from typing import Any



def filter_products(data: dict[str, Any]) -> BaseManager[Product]:
    if data['category'] and data['brand']:
        return Product.objects.all().order_by(data['sort_by']).filter(Q(price__gt=data['price__min']) & Q(price__lt=data['price__max']) & Q(category__in=data['category']) & Q(brand__in=data['brand']))
    elif not data['category'] and not data['brand']:
        return Product.objects.all().order_by(data['sort_by']).filter(Q(price__gt=data['price__min']) & Q(price__lt=data['price__max']))
    elif not data['category']:
        return Product.objects.all().order_by(data['sort_by']).filter(Q(price__gt=data['price__min']) & Q(price__lt=data['price__max']) & Q(brand__in=data['brand']))
    elif not data['brand']:
        return Product.objects.all().order_by(data['sort_by']).filter(Q(price__gt=data['price__min']) & Q(price__lt=data['price__max']) & Q(category__in=data['category']))
    
def filter_products_by_slug_of_category(data: dict[str, str]) -> BaseManager[Product]:
    return Product.objects.filter(category__slug=data['category'])
    

def pop_session_data(request: HttpRequest, key: str, exception: Any):
    value = request.session.get(key, exception)
    if key in request.session:
        del request.session[key]
    return value