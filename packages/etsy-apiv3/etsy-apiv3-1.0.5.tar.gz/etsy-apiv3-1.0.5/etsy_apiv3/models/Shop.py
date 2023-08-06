from __future__ import annotations
from dataclasses import dataclass
from pydantic import BaseModel
from typing import List, Optional

from etsy_apiv3.utils.APIV3 import EtsyAuth
from etsy_apiv3.utils.Response import Response

class Shop(BaseModel):
    shop_id: int
    user_id: int
    shop_name: str
    create_date: int
    title: Optional[str]
    announcement: Optional[str]
    currency_code: str
    is_vacation: bool
    vacation_message: Optional[str]
    sale_message: Optional[str]
    digital_sale_message: Optional[str]
    update_date: int
    listing_active_count: int
    digital_listing_count: int
    login_name: str
    accepts_custom_requests: bool
    policy_welcome: Optional[str]
    policy_payment: Optional[str]
    policy_shipping: Optional[str]
    policy_refunds: Optional[str]
    policy_additional: Optional[str]
    policy_seller_info: Optional[str]
    policy_update_date: int
    policy_has_private_receipt_info: bool
    has_unstructured_policies: bool
    policy_privacy: Optional[str]
    vacation_autoreply: Optional[str]
    url: str
    image_url_760x100: Optional[str]
    num_favorers: int
    languages: List[str]
    icon_url_fullxfull: Optional[str]
    is_using_structured_policies: bool
    has_onboarded_structured_policies: bool
    include_dispute_form_link: bool
    is_direct_checkout_onboarded: bool
    is_etsy_payments_onboarded: bool
    is_calculated_eligible: bool
    is_opted_in_to_buyer_promise: bool
    is_shop_us_based: bool
    transaction_sold_count: int
    shipping_from_country_iso: Optional[str]
    shop_location_country_iso: Optional[str]
    review_count: Optional[int]
    review_average: Optional[float]
    
