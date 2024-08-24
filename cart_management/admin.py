from django.contrib import admin

from .models import *

admin.site.register(Cart)
admin.site.register(WishList)
admin.site.register(CartOrderProduct)
admin.site.register(WishListOrderProduct)