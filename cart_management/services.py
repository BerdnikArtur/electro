from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404

from .models import CartOrderProduct, WishListOrderProduct
from .forms import AddToWishlistForm, AddToCartForm

from shop.models import Product

import json


class ItemCollectionService:

    @staticmethod
    def delete_button_item_collection_service(request: HttpRequest) -> JsonResponse:
        data = json.load(request)
        item_id = data['item']
        type_of_collection = data['type']

        if type_of_collection == WishListOrderProduct.__name__:
            order_product = get_object_or_404(WishListOrderProduct, pk=item_id)
            item_collection = order_product.wishlist if hasattr(order_product, 'wishlist') else None
        elif type_of_collection == CartOrderProduct.__name__:
            order_product = get_object_or_404(CartOrderProduct, pk=item_id)
            item_collection = order_product.cart if hasattr(order_product, 'cart') else None
        else:
            return JsonResponse({'status': 'error', 'message': 'Item not associated with any collection'}, status=400)

        if item_collection is None:
            return JsonResponse({'status': 'error', 'message': 'Collection not found'}, status=404)

        # Compute the price and quantity changes
        qty = item_collection.quantity - order_product.qty
        price = order_product.product.get_price_with_discount() * order_product.qty
        response_data = {
            'qty': str(qty),
            'qty-2': f'{qty} Item(s) selected',
            'subtotal': f'SUBTOTAL: ${item_collection.total_price - price}',
        }

        # Delete the item from the collection
        item_collection.delete_item(item_id)

        return JsonResponse(response_data)

    @staticmethod
    def add_to_item_collection(request: HttpRequest) -> JsonResponse:
        data = json.loads(request.body.decode('utf-8'))
        type_of_collection = data.get('type-collection')
        product = Product.objects.get(pk=data.get('product'))

        if type_of_collection == WishListOrderProduct.__name__:
            data['wishlist'] = request.user.wishlist.pk
            form = AddToWishlistForm(data, object=product, wishlist_pk=request.user.wishlist.pk)
        elif type_of_collection == CartOrderProduct.__name__:
            data['cart'] = request.user.cart.pk
            form = AddToCartForm(data, object=product, cart_pk=request.user.cart.pk)
        else:
            return JsonResponse({'status': 'error', 'message': 'Item not associated with any collection'}, status=400)


        if form.is_valid():
            form.save()

            collection_item = form.cleaned_data["product"]

            items_of_collection = { 
                "name": collection_item.name,
                "price_with_discount": collection_item.get_price_with_discount(),
                "price": collection_item.price,
                "imageUrl": collection_item.image.url,
                "url": collection_item.get_absolute_url(),
            }
                
            return JsonResponse({'status': "success", 'item_of_wishlist': items_of_collection})
