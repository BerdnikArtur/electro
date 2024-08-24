from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *

class ProductSizesInline(admin.TabularInline):
    model = ProductSizes
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductSizesInline]
    list_display = ('pk', 'name', 'image_of_product', 'price', 'category', 'seller',)
    search_fields = ('name', 'brand', 'category__name')
    fields = ('name', 'description', 'details', 'brand', 'image', 'image_of_product', 'price', 'discount', 'in_stock', 'seller', 'category')
    readonly_fields = ('slug', 'image_of_product', 'time_created', 'time_updated')

    def image_of_product(self, object):
        return mark_safe(f"<img src='{object.image.url}' width=50>")


admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductSizes)
admin.site.register(MultipleProductImages)
