from django.shortcuts import redirect

from .services import *

def delete_button_cart(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax and request.method == 'POST':
        return delete_button_item_collection_service(request)

    return redirect('home')

def delete_button_wishlist(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax and request.method == 'POST':
        return delete_button_item_collection_service(request)

    return redirect('home')

def add_to_wishlist(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return add_to_item_collection(request)
    
    return JsonResponse({"status": "error", "message": "Invalid data"})

def add_to_cart(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return add_to_item_collection(request)
    
    return JsonResponse({"status": "error", "message": "Invalid data"})


def add_to_compare(request):
    return JsonResponse({'status': "success"})