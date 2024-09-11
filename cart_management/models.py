from django.db import models, transaction
from django.utils.translation import gettext as _
from django.http import Http404

from .managers import ItemCollectionManager

class ItemCollection(models.Model):
    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    quantity = models.PositiveBigIntegerField(default=0)
    customer = models.OneToOneField("user_management.CustomUser", on_delete=models.CASCADE)

    objects = ItemCollectionManager()
    
    class Meta:
        abstract = True
    

class Cart(ItemCollection):
    
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
