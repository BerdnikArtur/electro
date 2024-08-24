from django.shortcuts import render, redirect
from django.http import JsonResponse

from .services.services import newsletter_service

import json

def newsletter(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax and request.method == 'POST':
        return newsletter_service(request)

    return redirect('home')
