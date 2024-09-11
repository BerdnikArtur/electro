from django import forms
from django.core.exceptions import ValidationError

from .models import CartOrderProduct, WishListOrderProduct
from shop.models import Product, ProductSizes

class BaseProductForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.object = kwargs.pop('object', None)
        super().__init__(*args, **kwargs)

        if self.object is not None:
            self._populate_product_fields()


    def _populate_product_fields(self):
        product_sizes = self.object.product_sizes.all() #seperate sql requests for cart and wishlist model
        self.fields['size'].choices = [(option.id, option.size) for option in product_sizes]
        self.fields['color'].choices = [(color, color) for color in self.object.color]
        self.fields['product'].initial = self.object.pk

    def clean(self):
        cleaned_data = super().clean()
        size_id = self.cleaned_data.get('size')
        product = self.cleaned_data.get('product')

        if size_id and not ProductSizes.objects.filter(id=size_id, product=product).exists():
            raise ValidationError("The selected size is not available for the chosen product.")
        cleaned_data['size'] = ProductSizes.objects.get(id=size_id) if size_id else None

        return cleaned_data

    class Meta:
        abstract = True

class AddToCartForm(BaseProductForm):
    def __init__(self, *args, **kwargs):
        self.cart_pk = kwargs.pop('cart_pk', None)
        super().__init__(*args, **kwargs)
        if self.cart_pk is not None and 'cart' in self.fields:
            self.fields['cart'].initial = self.cart_pk

    size = forms.ChoiceField(widget=forms.Select(attrs={'class': 'input-select', 'id': 'size'}))
    color = forms.ChoiceField(widget=forms.Select(attrs={'class': 'input-select', 'id': 'color'}))
    qty = forms.IntegerField(widget=forms.NumberInput(attrs={'value': '1'}))

    class Meta:
        model = CartOrderProduct
        fields = ['size', 'color', 'qty', 'product', 'cart']

class AddToWishlistForm(BaseProductForm):
    def __init__(self, *args, **kwargs):
        self.wishlist_pk = kwargs.pop('wishlist_pk', None)
        super().__init__(*args, **kwargs)
        if self.wishlist_pk is not None and 'wishlist' in self.fields:
            self.fields['wishlist'].initial = self.wishlist_pk

    size = forms.ChoiceField(widget=forms.Select(attrs={'class': 'input-select', 'id': 'size'}), required=False)
    color = forms.ChoiceField(widget=forms.Select(attrs={'class': 'input-select', 'id': 'color'}), required=False)
    qty = forms.IntegerField(widget=forms.NumberInput(attrs={'value': '1'}), required=False)

    class Meta:
        model = WishListOrderProduct
        fields = ['size', 'color', 'qty', 'product', 'wishlist']
