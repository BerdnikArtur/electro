from django import template
from django.http import HttpRequest
from django.db.models.manager import BaseManager
#from django.utils import timezone

from shop.models import *

from datetime import datetime, timedelta
from typing import Any

register = template.Library()

@register.filter
def int_to_range(value: int) -> range:
    return range(value)
    
@register.filter
def get_price_with_discount(item: Product) -> bool:
    if item.discount:
        return "{:.2f}".format(item.price - (item.price / 100) * item.discount)
    else:
        return item.price
    
@register.filter
def get_status_of_new(item: Product) -> bool:
    yesterday = datetime.today() - timedelta(weeks=1)
        
    if item.time_created.timestamp() >= yesterday.timestamp():
        return True
    else:
        return False
    
@register.filter
def absolute_url(req: HttpRequest, product: Product) -> str:
    return req.build_absolute_uri(product.get_absolute_url())
    