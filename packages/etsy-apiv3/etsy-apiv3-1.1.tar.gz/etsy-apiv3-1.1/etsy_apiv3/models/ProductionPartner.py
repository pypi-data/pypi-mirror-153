from pydantic import BaseModel

class ProductionPartner(BaseModel):
    production_partner_id: int
    partner_name: str
    location: str