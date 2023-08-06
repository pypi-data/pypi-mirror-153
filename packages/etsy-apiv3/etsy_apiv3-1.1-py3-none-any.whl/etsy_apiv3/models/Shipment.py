from __future__ import annotations
from pydantic import BaseModel

class Shipment(BaseModel):
    receipt_shipping_id: int
    shipment_notification_timestamp: int
    carrier_name: str
    tracking_code: str