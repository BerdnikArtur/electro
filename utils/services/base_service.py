from django.db.models.manager import BaseManager
from django.db.models import Prefetch
from django.http import HttpRequest

from shop.models import Category, Product, ProductSizes
from shop.forms import SearchForm
from cart_management.models import CartOrderProduct, WishListOrderProduct

from utils.mixins.cache_mixin import BaseCachingMixin


class BaseService(BaseCachingMixin):

    @staticmethod
    def _get_header_and_footer(request: HttpRequest):
        context = dict()
        #context['header_search'] = Category.objects.all()
        context['navigation'] = Category.objects.order_by('count_of_deals')[:5]
        context['breadcrumb'] = request.path.split("/")
        context['search_bar'] = SearchForm(categories=Category.objects.all()[:10])

        if request.user.is_authenticated:
            context['cart_items'] = CartOrderProduct.objects.filter(cart=request.user.cart.pk).select_related('product__category')
            context['wishlist_items'] = WishListOrderProduct.objects.filter(wishlist=request.user.wishlist.pk).select_related('product__category')
     
        return context
    

    def get_header_and_footer(self, request: HttpRequest) -> dict:
        return BaseService._get_header_and_footer(request)
    
    
    def _get_top_selling(self, amount=None, indent=0) -> BaseManager[Product]:
        
        queryset = Product.objects.select_related('category').prefetch_related(
            Prefetch('product_sizes', queryset=ProductSizes.objects.all().distinct())
        )
        
        if amount:
            queryset = queryset.distinct()[indent:amount]
        else:
            queryset = queryset.distinct()

        return queryset
    
    def get_top_selling(self, amount=None, indent=0) -> BaseManager[Product]:
        return self.get_cached_data(f"top_selling_{amount}_{indent}", self._get_top_selling, amount=amount, indent=indent)
    
    
def get_header_and_footer(request: HttpRequest) -> dict:
    return BaseService._get_header_and_footer(request)