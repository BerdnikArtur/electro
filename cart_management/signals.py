from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from .models import *

# @receiver(pre_delete, sender=WishListOrderProduct)
# @receiver(pre_delete, sender=CartOrderProduct)
# def update_item_collection_on_delete(sender, instance, **kwargs):
#     if isinstance(instance, WishListOrderProduct):
#         item_collection = instance.wishlist
#     elif isinstance(instance, CartOrderProduct):
#         item_collection = instance.cart
#     else:
#         # Handle the case where the instance is neither a CartOrderProduct nor a WishListOrderProduct
#         return
    
#     item_collection.total_price -= instance.product.get_price_with_discount() * instance.qty
#     item_collection.quantity -= instance.qty
#     item_collection.save()

@receiver(post_save, sender="user_management.CustomUser")
def create_user_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(customer=instance)
        WishList.objects.create(customer=instance)


@receiver(post_save, sender=WishListOrderProduct)
@receiver(post_save, sender=CartOrderProduct)
def update_cart(sender, instance, created, **kwargs):
    if created:
        if isinstance(instance, WishListOrderProduct):
            item_collection = instance.wishlist
            WishList.objects.update_total_price_and_quantity(item_collection, price=instance.product.get_price_with_discount(), qty=instance.qty)
        elif isinstance(instance, CartOrderProduct):
            item_collection = instance.cart
            Cart.objects.update_total_price_and_quantity(item_collection, price=instance.product.get_price_with_discount(), qty=instance.qty)