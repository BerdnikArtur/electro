from django.shortcuts import redirect

from .services import *

def create_review(request, category, product):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax and request.method == 'POST':
        return ProductPageReviewsService.create_review(request)
    return redirect('home')

def load_reviews(request, category, product):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    if is_ajax and request.method == 'GET':
        return ProductPageReviewsService.load_reviews(request)
