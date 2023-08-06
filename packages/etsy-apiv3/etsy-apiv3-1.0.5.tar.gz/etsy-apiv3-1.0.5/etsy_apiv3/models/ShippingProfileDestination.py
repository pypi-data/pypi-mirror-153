from __future__ import annotations
from pydantic import BaseModel
from etsy_apiv3.models.Price import Price

class ShippingProfileDestination(BaseModel):
    shipping_profile_destination_id: int
    shipping_profile_id: int
    origin_country_iso: str
    destination_country_iso: str
    destination_region: str
    primary_cost: Price
    secondary_cost: Price
    shipping_carrier_id: int
    mail_class: str
    min_delivery_days: int
    max_delivery_days: int