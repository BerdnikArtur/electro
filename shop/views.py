from typing import Any
import json

from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin
from django.utils.translation import gettext as _
from django.http import HttpResponseRedirect, JsonResponse

from .forms import *
from .services import model_services
from .services.services import *


class HomePage(ListView):
    model = Product
    template_name = 'shop/index.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        return HomePageService.get_context_data(self.request, context)
    

class StorePage(ListView, FormMixin):
    model = Product
    template_name = 'shop/store.html'
    slug_url_kwargs = 'category'
    paginate_by = 9
    form_class = FiltersAside

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        return StorePageService.get_context_data(self.request, context, self.form_class)
    
    def get_queryset(self):
        return StorePageService.get_queryset(self.request, *self.args, **self.kwargs)
    
    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        
        request.session['category'] = model_services.get_category_slugs(request)
        #print([i.slug for i in Category.objects.filter(pk__in=request.POST.getlist('category', []))])
        
        return self.render_to_response(context)

class ProductPage(DetailView):
    model = Product
    template_name = 'shop/product.html'
    slug_field = "slug" 
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super(ProductPage, self).get_context_data(**kwargs)

        return ProductPageService.get_context_data(self.request, context, self.object)
    
    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        return ProductPageService.get_object(self.kwargs, queryset)
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.get_context_data(object=self.object)
        
        if request.method == 'POST':
            ProductPageService.post(request, self.object)

        return HttpResponseRedirect(self.object.get_absolute_url())


def search(request):
    query = request.GET.get('query', '')
    category_id = request.GET.get('category', 0)

    #Any logic

    request.session['search-query'] = query
    request.session['search-category'] = category_id

    return HttpResponseRedirect(reverse_lazy('store'))