from dataclasses import dataclass
from etsy_apiv3.models.Shop import Shop
from etsy_apiv3.utils.APIV3 import EtsyAuth
from etsy_apiv3.utils.Response import Response

@dataclass
class ShopResource:
    """
    Shop Resource Of Etsy Api V3.

    """
    auth: EtsyAuth
    
    def get_shop(self, shop_id: int):
        """
        Get Shop By Shop Id And Return A Shop Object

        Args:
            shop_id (int): Shop Id

        Returns:
            Shop: Shop Object
        """
        
        endpoint = f"shops/{shop_id}"
        response = self.auth.request(endpoint)
        return Shop(**response)
    
    def find_shops(self):
        """
        Find All Shops And Return Response Object
        
        Returns:
            Response: Return Response object of shop list 
        """
        endpoint = "shops/"
        response = self.auth.request(endpoint)
        return Response[Shop](**response)

    def find_shop_by_owner_user_id(self, user_id: int):
        """
        Find Shop By Owner User Id And Return A Shop Object.

        Args:
            user_id (int): Shop Owner User Id

        Returns:
            Shop: Return A Shop Object
        """
        endpoint = f"users/{user_id}/shops"
        response = self.auth.request(endpoint)
        return Shop(**response)
    
    def update_shop(self, shop_id: int, title: str = "", announcement: str = "", sale_message: str = "", digital_sale_message: str = ""):
        endpoint = f"shops/{shop_id}"
        pass