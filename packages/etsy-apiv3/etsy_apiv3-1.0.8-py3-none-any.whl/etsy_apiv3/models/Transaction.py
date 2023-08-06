from __future__ import annotations
from pydantic import BaseModel
from typing import List, Optional
from etsy_apiv3.models.Price import Price
from etsy_apiv3.models.Variation import Variation

class Transaction(BaseModel):
    transaction_id: int
    title: str
    description: str
    seller_user_id: int
    buyer_user_id: int
    create_timestamp: int
    paid_timestamp: Optional[int]
    shipped_timestamp: Optional[int]
    quantity: int
    listing_image_id: int
    receipt_id: int
    is_digital: bool
    file_data: str
    listing_id: int
    transaction_type: str
    product_id: int
    sku: str
    price: Price
    shipping_cost: Price
    variations: List[Variation]
    shipping_profile_id: Optional[int]
    min_processing_days: Optional[int]
    max_processing_days: Optional[int]
    shipping_method: Optional[str]
    shipping_upgrade: Optional[str]
    expected_ship_date: Optional[int]
    
