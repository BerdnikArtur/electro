from django.db import models, transaction
from django.utils.translation import gettext as _
from django.http import Http404


class ItemCollection(models.Model):
    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    quantity = models.PositiveBigIntegerField(default=0)
    customer = models.OneToOneField("user_management.CustomUser", on_delete=models.CASCADE)

    @transaction.atomic
    def update_total_price_and_quantity(self, price=None, qty=None) -> None:
        if price is not None and qty is not None:
            try:
                self.total_price += price * qty
                self.quantity += qty
            except (TypeError, ValueError):
                raise Http404(_(f"price and quantity of {self.__class__.__name__} must be decimal and integer accordingly"))
        else:
            cart_items = self.orderproduct_set.all()
            total_price = sum(item.product.get_price_with_discount() * item.qty for item in cart_items)
            quantity = sum(item.qty for item in cart_items)
            self.total_price = total_price
            self.quantity = quantity

        self.save()

    def delete_item(self, item_pk: int) -> None:
        item = self.orderproduct_set.get(pk=item_pk)
        self.total_price -= item.product.get_price_with_discount() * item.qty
        self.quantity -= item.qty
        item.delete()
        self.save()

    def delete(self, *args, **kwargs):
        #self.total_price = 0
        #self.quantity = 0
        super().delete(*args, **kwargs)
    
    class Meta:
        abstract = True
    

class Cart(ItemCollection):

    def get_list_of_parcels(self):
        parcels = []
        order_products = self.orderproduct_set.all()

        for order_product in order_products:
            if order_product.size:
                parcel_data = order_product.size.to_shippo_parcel()

                for _ in range(order_product.qty):
                    parcels.append(parcel_data)
            else:
                raise ValueError(f"Order product {order_product.id} does not have a size assigned.")
                
        return parcels
    
    def __str__(self):
        return f"{self.customer.username}'s cart"
    

class WishList(ItemCollection):

    def __str__(self):
        return f"{self.customer.username}'s wishlist"


class AbstractOrderProduct(models.Model):
    color = models.CharField(max_length=225, null=True, blank=True)
    qty = models.PositiveBigIntegerField(default=1, blank=True)

    product = models.ForeignKey("shop.Product", on_delete=models.CASCADE)
    size = models.ForeignKey("shop.ProductSizes", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.product.name} - {self.size.size if self.size else 'No size'}"

    class Meta:
        abstract = True


class CartOrderProduct(AbstractOrderProduct):
    cart = models.ForeignKey('Cart', related_name='orderproduct_set', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Cart\'s order-product'
        verbose_name_plural = 'Cart\'s order-products'


class WishListOrderProduct(AbstractOrderProduct):
    wishlist = models.ForeignKey('WishList', related_name='orderproduct_set', on_delete=models.CASCADE)
    size = models.ForeignKey("shop.ProductSizes", on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'Wishlist\'s order-product'
        verbose_name_plural = 'Wishlist\'s order-products'
