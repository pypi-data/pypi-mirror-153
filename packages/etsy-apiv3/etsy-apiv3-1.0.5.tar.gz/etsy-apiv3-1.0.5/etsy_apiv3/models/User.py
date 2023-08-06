from __future__ import annotations
from pydantic import BaseModel

class User(BaseModel):
    user_id: int
    login_name: str
    primary_email: str
    first_name: str
    last_name: str
    create_timestamp: int
    referred_by_user_id: int
    use_new_inventory_endpoints: bool
    is_seller: bool
    bio: str
    gender: str
    birth_month: str
    birth_day: str
    transaction_buy_count: int
    transaction_sold_count: int