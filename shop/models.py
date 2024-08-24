from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext as _
from django.contrib.postgres.fields import ArrayField

from shippo import components

class Category(models.Model):
    '''
    Simple model for categories, there is no anything complex
    '''
    name = models.CharField(max_length=225)
    slug = models.SlugField(unique=True, editable=False)

    count_of_deals = models.PositiveBigIntegerField(default=0, editable=False, db_index=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    # extend save function of model.Model, create slug with slugify function while using save()
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('category', kwargs={'category': self.slug})
    
    def __str__(self):
        return self.name


def default_colors():
    return ["black", "white", "blue"]

class Product(models.Model):
    '''
    Model of products 
    '''
    BLACK = "black"
    WHITE = "white"
    BLUE = "blue"

    COLOR_CHOICES = {
        BLACK: "black",
        WHITE: "white",
        BLUE: "blue",
    }

    name = models.CharField(max_length=225)
    slug = models.SlugField(unique=True, editable=False)

    description = models.TextField(blank=False)
    details = models.TextField(blank=False)
    brand = models.CharField(max_length=225, null=True)

    image = models.ImageField(upload_to='shop/images/%y%m%d', blank=False)

    # discount saved as a percentage, price field uses decimal so essentially there is no currency
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=False)
    discount = models.PositiveSmallIntegerField(default=0)

    color = ArrayField(models.CharField(max_length=225, choices=COLOR_CHOICES, default=BLACK), default=default_colors)

    in_stock = models.PositiveSmallIntegerField(default=1)
    count_of_selled = models.PositiveSmallIntegerField(default=0, editable=False, db_index=True) 

    time_created = models.DateTimeField(auto_now_add=True, editable=False)
    time_updated = models.DateTimeField(auto_now=True, editable=False)

    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    seller = models.ForeignKey("user_management.CustomUser", on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('product', kwargs={'category': self.category.slug, 'product': self.slug})
    
    def get_price_with_discount(self):
        if self.discount:
            new_price = self.price - (self.price / 100) * self.discount
        else:
            new_price = self.price
        return new_price 
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['-time_created', 'name']

class ProductSizes(models.Model):
    size = models.CharField(max_length=225)  

    length = models.DecimalField(max_digits=10, decimal_places=2)
    width = models.DecimalField(max_digits=10, decimal_places=2)
    height = models.DecimalField(max_digits=10, decimal_places=2)
    weight = models.DecimalField(max_digits=10, decimal_places=2)

    product = models.ForeignKey("shop.Product", related_name="product_sizes", on_delete=models.CASCADE)

    def to_shippo_parcel(self):
        return components.ParcelCreateRequest(
            length = f"{self.length}",  
            width = f"{self.width}",
            height = f"{self.height}",
            weight = f"{self.weight}",
            distance_unit = components.DistanceUnitEnum.IN,
            mass_unit = components.WeightUnitEnum.LB,
        )
    
    def __str__(self):
        return self.size

class MultipleProductImages(models.Model):
    image = models.ImageField(upload_to="shop/gallery_images/%y%m%d", null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

