from __future__ import annotations
from typing import Optional
from pydantic import BaseModel


class ListingImage(BaseModel):
    listing_image_id: int
    hex_code: Optional[str]
    red: Optional[int]
    green: Optional[int]
    blue: Optional[int]
    hue: Optional[int]
    saturation: Optional[int]
    brightness: Optional[int]
    is_black_and_white: Optional[bool]
    creation_tsz: int
    rank: int
    url_75x75: str
    url_170x135: str
    url_570xN: str
    url_fullxfull: str
    full_height: Optional[str]
    full_width: Optional[str]
    alt_text: Optional[str]