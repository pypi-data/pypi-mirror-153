from pydantic import BaseModel
from etsy_apiv3.models.Price import Price

class ShippingProfileUpgrade(BaseModel):
    shipping_profile_id: int
    upgrade_id: int
    upgrade_name: str
    type: str
    rank: int
    language: str
    price: Price
    secondary_price: Price
    shipping_carrier_id: int
    mail_class: str
    min_delivery_days: int
    max_delivery_days: int