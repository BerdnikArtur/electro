from django.db.models.manager import BaseManager
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest
from django.utils.safestring import SafeText

from shop.models import *
from review_management.models import ProductRating

from datetime import datetime, timedelta
from typing import Any

def get_hot_deals() -> BaseManager[Product]:
    hot_week = datetime.today() - timedelta(days=7)
    hot_deals = Product.objects.filter(time_created__gte=hot_week).select_related('category').prefetch_related('product_sizes')
    return hot_deals

def get_top_selling(amount=None, indent=0) -> BaseManager[Product]:
    if amount:
        top_selling = Product.objects.all()[indent:amount].select_related('category').prefetch_related('product_sizes')
    else:
        top_selling = Product.objects.all().select_related('category').prefetch_related('product_sizes')

    return top_selling

def get_slick_tablet(amount: int) -> list:
    slick_tablet = []
    for i in range(3, amount+3, 3):
         slick_tablet.append(get_top_selling(i, i-3))

    return slick_tablet

def get_categories(amount: int) -> Category:
    categories = Category.objects.all()[:amount]
    return categories

def get_brands(amount: int) -> list[str]:
    list_of_brands = ['SAMSUNG', 'LG', 'SONY', 'POCO', 'NVIDIA', 'AMD']
    return list_of_brands

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
    
def get_category_slugs(request: HttpRequest) -> list[str|SafeText]:
    return [i.slug for i in Category.objects.filter(pk__in=request.POST.getlist('category', []))]

def pop_session_data(request: HttpRequest, key: str, exception: Any):
    value = request.session.get(key, exception)
    if key in request.session:
        del request.session[key]
    return value