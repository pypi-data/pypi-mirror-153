from typing import List
from pydantic import BaseModel

class Translation(BaseModel):
    listing_id: int
    language: str
    title: str
    description: str
    tags: List[str]