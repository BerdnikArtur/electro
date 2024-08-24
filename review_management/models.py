from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

class ProductRating(models.Model):
    rating = models.DecimalField(max_digits=3, decimal_places=1, editable=False, null=True)
    one_star = models.PositiveSmallIntegerField(default=0, editable=False)
    two_star = models.PositiveSmallIntegerField(default=0, editable=False)
    three_star = models.PositiveSmallIntegerField(default=0, editable=False)
    four_star = models.PositiveSmallIntegerField(default=0, editable=False)
    five_star = models.PositiveSmallIntegerField(default=0, editable=False)
    product = models.OneToOneField('shop.Product', on_delete=models.CASCADE, related_name='product_rating')

    def update_rating(self, item, increase=True):
        match item:
            case 1:
                self.one_star += 1 if increase == True else -1
            case 2:
                self.two_star += 1 if increase == True else -1
            case 3:
                self.three_star += 1 if increase == True else -1
            case 4:
                self.four_star += 1 if increase == True else -1
            case 5:
                self.five_star += 1 if increase == True else -1

        total_reviews = self.one_star + self.two_star + self.three_star + self.four_star + self.five_star
        total_rating =  1 * self.one_star + 2 * self.two_star + 3 * self.three_star + 4 * self.four_star + 5 * self.five_star

        self.rating = total_rating / total_reviews if total_reviews > 0 else None

        self.save()

@receiver(post_save, sender='shop.Product')
def create_product_rating(sender, instance, created, **kwargs):
    if created:
        ProductRating.objects.create(product=instance)

class Review(models.Model):
    '''
    Model of reviews for products
    '''
    text = models.TextField()
    rating = models.PositiveSmallIntegerField()
    date_created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey("user_management.CustomUser", on_delete=models.CASCADE)
    product_rating = models.ForeignKey(ProductRating, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('review', kwargs={'category': self.product.category.slug, 'product': self.product.slug})

    def delete(self):
        self.product_rating.update_rating(self.rating, increase=False)
        super(Review, self).delete()
