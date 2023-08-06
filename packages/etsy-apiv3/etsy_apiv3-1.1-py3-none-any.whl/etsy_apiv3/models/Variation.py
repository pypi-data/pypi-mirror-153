from typing import Optional
from pydantic import BaseModel

class Variation(BaseModel):
    property_id: Optional[int]
    value_id: Optional[int]
    formatted_name: str
    formatted_value: str