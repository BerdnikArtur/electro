from django.shortcuts import get_object_or_404
from django.db.models.manager import BaseManager
from django.http import HttpRequest, Http404
from django.forms import BaseForm
from django.db.models import QuerySet
from django.utils.translation import gettext as _

from .model_services import *
from ..forms import FiltersAside, SearchForm

from cart_management.forms import AddToCartForm, AddToWishlistForm
from cart_management.models import CartOrderProduct, WishListOrderProduct
from review_management.models import Review

def get_header_and_footer(request):
        context = dict()
        #context['header_search'] = Category.objects.all()
        context['navigation'] = Category.objects.order_by('count_of_deals')[:5]
        context['breadcrumb'] = request.path.split("/")
        context['search_bar'] = SearchForm(categories=Category.objects.all()[:10])

        if request.user.is_authenticated:
            context['cart_items'] = CartOrderProduct.objects.filter(cart=request.user.cart.pk)
            context['wishlist_items'] = WishListOrderProduct.objects.filter(wishlist=request.user.wishlist.pk).select_related('product__category')
    
        return context

class HomePageService:

    @staticmethod
    def get_context_data(request: HttpRequest, context: dict[str: Any]) -> dict[str: Any]:
        
        header_and_footer_context = get_header_and_footer(request)

        context['hot_deals'] = get_hot_deals()
        context['top_selling'] = get_top_selling(5)
        context['slick_tablet'] = get_slick_tablet(6)

        return {**header_and_footer_context, **context}

class StorePageService:
    
    @staticmethod
    def get_context_data(request: HttpRequest, context: dict[str: Any], form_class: type[BaseForm]) -> dict[str: Any]:
        
        header_and_footer_context = get_header_and_footer(request)

        context['filters_aside'] = form_class
        context['category_aside'] = get_categories(6)
        context['brands'] = get_brands(6)
        context['tablet_aside'] = get_top_selling(3)
        
        cookie = request.session.get('additional_data', None)
        if request.method == "GET" and cookie:
            context['checkbox_categories'] = [str(Category.objects.get(slug=request.session.get('category')).pk)]
        elif request.method == "POST":
            context['select_option_sort_by'] = request.POST.get('sort_by')
            context['checkbox_categories'] = request.POST.getlist('category', [])
            context['checkbox_brands'] = request.POST.getlist('brand', [])

        return {**header_and_footer_context, **context}

    @staticmethod
    def get_queryset(request: HttpRequest, *args, **kwargs) -> BaseManager[Product]:
        def get_session_data(request):
            return {
                "query": request.session.get("search-query"),
                "category_id": request.session.get("search-category", '0')
            }

        def clear_session_data(request):
            request.session.pop("search-query", None)
            request.session.pop("search-category", '0')

        def handle_post_request(request):
            form = FiltersAside(request.POST.copy())
            if form.is_valid():
                clear_session_data(request)
                return filter_products(form.cleaned_data)
            return get_top_selling()

        def handle_get_request(request, kwargs):
            clear_session_data(request)
            if kwargs:
                return filter_products_by_slug_of_category(data=kwargs)
            return get_top_selling()

        def handle_session_data(session_data):
            query = session_data["query"]
            category_id = session_data["category_id"]

            filters = Q()
            if query:
                filters &= Q(name__icontains=query)
            if category_id and category_id != '0':
                filters &= Q(category_id=category_id)
            
            if filters:
                return Product.objects.filter(filters).select_related('category')
            
            return get_top_selling()
        

        if request.method == 'POST':
            return handle_post_request(request)

        if request.method == 'GET':
            session_data = get_session_data(request)

            clear_session = request.GET.get('clear_session', 'false').lower() == 'true'
            
            if clear_session:
                clear_session_data(request)
                return handle_get_request(request, kwargs)

            if session_data["query"] or session_data["category_id"] != '0':
                return handle_session_data(session_data)
            return handle_get_request(request, kwargs)

        return get_top_selling()

    @staticmethod
    def post(request: HttpRequest) -> dict[str: Any]:
        return {
            'select_option_sort_by': request.POST.get('sort_by'),
            'checkbox_categories': request.POST.getlist('category', []),
            'checkbox_brands': request.POST.getlist('brand', []),
        }
    
class ProductPageService:

    @staticmethod
    def get_context_data(request: HttpRequest, context: dict[str: Any], object: Any) -> dict[str: Any]:
        header_and_footer = get_header_and_footer(request)

        context['product_images'] = MultipleProductImages.objects.filter(product=object)
        context['related_products'] = Product.objects.filter(brand=object.brand)[:10].select_related('category')
        context['reviews'] = Review.objects.filter(product_rating=object.product_rating).order_by("-date_created")[:5].select_related('user')
        context['rating'] = object.product_rating

        if request.user.is_authenticated:
            context['add_to_cart'] = AddToCartForm(object=object, cart_pk=request.user.cart.pk)
            context['add_to_wishlist'] = AddToWishlistForm(object=object, wishlist_pk=request.user.wishlist.pk) 
 
        return {**header_and_footer, **context}

    @staticmethod
    def get_object(data_kwargs: Any, queryset: QuerySet[Any]) -> Any:
        category_slug = data_kwargs.get('category', None)
        product_slug = data_kwargs.get('product', None)
        try:
            obj = queryset.get(category__slug=category_slug, slug=product_slug)
        except queryset.model.DoesNotExist:
            raise Http404(_("No product found matching the query"))
        return obj

    @staticmethod
    def post(request: HttpRequest, object: Any) -> None:
        data = request.POST.copy()
        data['product'] = object.pk
        data['cart'] = request.user.cart.pk
        form = AddToCartForm(data, object_pk=object.pk, cart_pk=request.user.cart.pk)
        if form.is_valid():
            form.save() 