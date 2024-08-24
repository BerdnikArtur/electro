from django.views.generic import FormView
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import CheckoutForm
from .services.services import *

from typing import Any

class CheckoutPage(LoginRequiredMixin, FormView):
    form_class = CheckoutForm
    template_name = 'order_management/checkout.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('login')
    raise_exception = True

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return CheckoutService.get_context_data(self.request, context)

    def form_valid(self, form):
        if self.request.method == 'POST' and self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            self.extra_context = CheckoutService.form_valid(self.request, form)
            return JsonResponse({'status': 'succeed'})
        
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.method == 'POST' and self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'error', 'message': form.errors})

        return super().form_invalid(form)