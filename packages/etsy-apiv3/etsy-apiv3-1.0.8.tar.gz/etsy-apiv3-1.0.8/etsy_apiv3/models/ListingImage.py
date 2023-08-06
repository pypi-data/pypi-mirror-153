from __future__ import annotations
from pydantic import BaseModel


class ListingImage(BaseModel):
    listing_image_id: int
    hex_code: str
    red: int
    green: int
    blue: int
    hue: int
    saturation: int
    brightness: int
    is_black_and_white: bool
    creation_tsz: int
    rank: int
    url_75x75: str
    url_170x135: str
    url_570xN: str
    url_fullxfull: str
    full_height: int
    full_width: int