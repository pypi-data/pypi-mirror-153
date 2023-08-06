from dataclasses import dataclass
from etsy_apiv3.utils.APIV3 import EtsyAuth
from etsy_apiv3.utils.Response import Response
from etsy_apiv3.models.Review import Review

@dataclass
class ReviewResource:
    auth: EtsyAuth
    
    def get_reviews_by_listing_id(self, listing_id: int, limit: int = 25, offset: int = 0):
        
        params = {"limit": limit, "offset": offset}
        url = f"listings/{listing_id}/reviews"
        
        response = self.auth.request(url, params=params)
        return Response[Review](**response)
    
    def get_reviews_by_shop_id(self, shop_id: int, limit: int = 25, offset: int = 0):
        
        params = {"limit": limit, "offset": offset}
        url = f"shops/{shop_id}/reviews"
        
        response = self.auth.request(url, params=params)
        return Response[Review](**response)