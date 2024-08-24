from django.db import models
from django.utils.translation import gettext as _
from django.core.validators import RegexValidator


class BillingAddress(models.Model):
    '''
    Model for orders
    '''

    first_name = models.CharField(max_length=225)
    last_name = models.CharField(max_length=225)

    address = models.CharField(max_length=225)
    city = models.CharField(max_length=225)
    state = models.CharField(max_length=225)
    country = models.CharField(max_length=225)

    zip_code = models.CharField(max_length=10)
    telephone = models.CharField(validators=[RegexValidator(regex=r'^(071)\d{9}$')], max_length=15, null=True, blank=True)

    order = models.ForeignKey("order_management.Order", on_delete=models.CASCADE)

    def to_shippo_address(self):
        return {
            "name": f"{self.first_name} {self.last_name}",
            "street1": self.address, 
            "city": self.city,
            "state": self.state,
            "zip": self.zip_code,
            "country": self.country,
            "phone": self.telephone
        }

class Order(models.Model):
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"

    STATUS_CHOICES = {
        PROCESSING: "Processing",
        SHIPPED: "Shipped",
        DELIVERED: "Delivered",
    }

    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    stripe_payment_intent_id = models.CharField(max_length=100)

    tracking_number = models.CharField(max_length=100, blank=True, null=True)
    shipment_id = models.CharField(max_length=100, blank=True, null=True)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    label_url = models.URLField(max_length=2000, blank=True, null=True)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PROCESSING)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    user = models.ForeignKey("user_management.CustomUser", on_delete=models.CASCADE)

    def __str__(self):
        return f"Order {self.id}"
