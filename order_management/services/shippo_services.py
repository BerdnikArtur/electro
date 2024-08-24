import shippo
from shippo.models import components
from django.conf import settings


class ShippoService:
    shippo_sdk = shippo.Shippo(api_key_header=settings.SHIPPO_API_KEY)

    @staticmethod
    def create_shipment(from_address: dict, to_address: dict, parcels:list[dict]):
        shipment = ShippoService.shippo_sdk.shipments.create(
            components.ShipmentCreateRequest(
                address_from=components.AddressCreateRequest(**from_address),
                address_to=components.AddressCreateRequest(**to_address),
                parcels=parcels,#[components.ParcelCreateRequest(**parcel)],
                async_=False
            )
        )

        if shipment.object_id == None:
            raise Exception('Error creating shipment with Shippo')

        return shipment

    @staticmethod
    def create_transaction(shipment):
        if not shipment.rates:
            raise Exception('No shipping rates available for this shipment')
        
        rate = shipment.rates[0]

        transaction = ShippoService.shippo_sdk.transactions.create(
            components.TransactionCreateRequest(
                rate=rate.object_id,
                label_file_type=components.LabelFileType.PDF,
                async_=False
            )
        )

        print(transaction)
        if transaction.status != "SUCCESS":
            raise Exception('Error creating transaction with Shippo')

        return transaction