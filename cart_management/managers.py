from django.db import models, transaction
from django.http import Http404
from django.utils.translation import gettext_lazy as _

class ItemCollectionManager(models.Manager):
    
    @transaction.atomic
    def update_total_price_and_quantity(self, item_collection, price=None, qty=None):
        if price is not None and qty is not None:
            try:
                item_collection.total_price += price * qty
                item_collection.quantity += qty
            except (TypeError, ValueError):
                raise Http404(_(f"price and quantity of {item_collection.__class__.__name__} must be decimal and integer accordingly"))
        else:
            cart_items = item_collection.orderproduct_set.all()
            total_price = sum(item.product.get_price_with_discount() * item.qty for item in cart_items)
            quantity = sum(item.qty for item in cart_items)
            item_collection.total_price = total_price
            item_collection.quantity = quantity

        item_collection.save()

    def delete_item(self, item_collection, item_pk: int):
        item = item_collection.orderproduct_set.get(pk=item_pk)
        item_collection.total_price -= item.product.get_price_with_discount() * item.qty
        item_collection.quantity -= item.qty
        item.delete()
        item_collection.save()

    def get_list_of_parcels(self, item_collection):
        parcels = []
        order_products = item_collection.orderproduct_set.all()

        for order_product in order_products:
            if order_product.size:
                parcel_data = order_product.size.to_shippo_parcel()
                for _ in range(order_product.qty):
                    parcels.append(parcel_data)
            else:
                raise ValueError(f"Order product {order_product.id} does not have a size assigned.")
                
        return parcels
