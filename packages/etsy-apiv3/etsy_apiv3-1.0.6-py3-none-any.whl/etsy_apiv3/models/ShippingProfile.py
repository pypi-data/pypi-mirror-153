from pydantic import BaseModel
from etsy_apiv3.models.Price import Price
from typing import List
from etsy_apiv3.models.ShippingProfileUpgrade import ShippingProfileUpgrade
from etsy_apiv3.models.ShippingProfileDestination import ShippingProfileDestination


class ShippingProfile(BaseModel):
    shipping_profile_id: int
    title: str
    user_id: int
    min_processing_days: int
    max_processing_days: int
    processing_days_display_label: str
    origin_country_iso: str
    is_deleted: bool
    shipping_profile_destinations: List[ShippingProfileDestination]
    shipping_profile_upgrades: List[ShippingProfileUpgrade]
    origin_postal_code: str
    profile_type: str
    domestic_handling_fee: int
    international_handling_fee: int