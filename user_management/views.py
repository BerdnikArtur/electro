from django.forms import BaseModelForm
from django.shortcuts import redirect, HttpResponseRedirect
from django.http import HttpResponse, JsonResponse
from django.views.generic import CreateView
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

from typing import Any

from .forms import RegisterUserForm, LoginUserForm

from .services import *

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'user_management/register.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return register_user_get_context_data(self.request, context)
    
    def form_valid(self, form: BaseModelForm) -> JsonResponse:
        if self.request.method == 'POST' and self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            object = form.save()
            login(self.request, object)
            return JsonResponse({'status': 'succeed'})
        return super().form_valid(form)
    
    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        if self.request.method == 'POST' and self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'error', 'message': f'{form.errors}'})
        return super().form_invalid(form)
    
class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'user_management/login.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        return login_user_get_context_data(self.request, context)

    def get_success_url(self):
        return reverse_lazy('home')
    
def logout_user(request):
    logout(request)
    return redirect('home')
