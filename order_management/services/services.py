from typing import Any

from django.http import HttpRequest
from django.forms import BaseForm

from ..models import *

from shop.services.services import get_header_and_footer
from payment_management.services import stripe_service
from .shippo_services import ShippoService


class CheckoutService:
    @staticmethod
    def get_context_data(request: HttpRequest, context: dict[str: Any]) -> dict[str: Any]:
        return {**get_header_and_footer(request), **context}
    
    @staticmethod
    def form_valid(request: HttpRequest, form: BaseForm):
        intent = stripe_service.create_payment_intent(request.user.cart.total_price)
        order = Order.objects.create(
            user=request.user,
            total_amount=request.user.cart.total_price,
            stripe_payment_intent_id=intent['id']
        )
        
        billing_address = form.save(commit=False)
        billing_address.order = order
        billing_address.save()
            
        try:
            #default sender address
            sender_address = {
                "name":"Shawn Ippotle",
                "email":"randomuser1234@example.com",
                "street1":"215 Clayton St.",
                "city":"San Francisco",
                "state":"CA",
                "zip":"94117",
                "country":"US",
                "phone":"(555) 123-4567",
            }

            recipient_address = billing_address.to_shippo_address()
            
            list_of_parcels = request.user.cart.get_list_of_parcels()
            
            # Create Shipment with Shippo
            shipment = ShippoService.create_shipment(sender_address, recipient_address, list_of_parcels)
            
            # Create Transaction with Shippo
            transaction = ShippoService.create_transaction(shipment)
            
            # Save shipment and transaction details to the order
            order.tracking_number = transaction.tracking_number
            order.shipment_id = shipment.object_id
            order.transaction_id = transaction.object_id
            order.label_url = transaction.label_url
            order.shipping_cost = shipment.rates[0].amount
            order.save()

            # Pass client secret and order_id to context for the payment step
            extra_context = {
                'client_secret': intent['client_secret'],
                'order_id': order.id
            }

            return extra_context
        except Exception as error:
            print(error)
            order.delete()
            billing_address.delete()
            
    
