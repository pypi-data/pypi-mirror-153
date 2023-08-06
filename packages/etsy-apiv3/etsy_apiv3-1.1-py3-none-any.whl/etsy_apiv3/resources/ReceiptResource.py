from dataclasses import dataclass
from etsy_apiv3.utils.APIV3 import EtsyAuth
from etsy_apiv3.utils.Response import Response
from etsy_apiv3.models.Receipt import Receipt, ReceiptType

@dataclass
class ReceiptResource:
    """
    Receipt Resource is the utility class to get receipts from Etsy
    
    Attributes:
        auth (EtsyAuth): EtsyAuth Object
        
    """
    
    __endpoint = "shops/{shop_id}/receipts"
    auth: EtsyAuth
    
    
    
    def find(self, shop_id: int, limit=25, offset=0, type: ReceiptType = ReceiptType.UNSHIPPED) -> Response[Receipt]:
        """
        Find Receipts By Shop ID And Receipt Type

        Args:
            
            shop_id (int): Your SHOP ID
            limit (int, optional): Limit Of Receipt Objects. Defaults to 25.
            offset (int, optional): How many receipts to skip. Defaults to 0.
            type (ReceiptType, optional): Receipt type to find. Defaults to ReceiptType.UNSHIPPED.

        Returns:
            Response[Receipt]: Create Response Object Derived from the Receipt Object from json
        """
        
        endpoint = self.__endpoint.format(shop_id=shop_id)
        
        params = {"limit":limit, "offset":offset}
        params.update(type)
        json = self.auth.request(endpoint=endpoint, params=params)
        
        return Response[Receipt](**json)
    
    def find_one(self, shop_id: int, receipt_id: int):
        """
        Find One Receipt By Shop ID And Receipt ID

        Args:
            shop_id (int): Your SHOP ID
            receipt_id (int): Receipt ID
            
        Returns:
            Receipt: Create Receipt Object from json
        """
        endpoint = f"{self.__endpoint.format(shop_id=shop_id)}/{receipt_id}"
        json = self.auth.request(endpoint=endpoint)
        
        return Receipt(**json)

    def create_shipment(self, shop_id: int, receipt_id: int, tracking_number: str, carrier_name: str, send_bcc: bool = True, note_to_buyer: str = ""):
        """
        Adds tracking information to the receipt object

        Args:
            shop_id (int): SHOP ID
            receipt_id (int): Target Receipt ID
            tracking_number (str): Tracking Number
            carrier_name (str): Carrier Name Ex: UPS
            send_bcc (bool, optional): Send Mail. Defaults to True.
            note_to_buyer (str, optional): Note To Buyer From Seller. Defaults to "".

        Returns:
            Receipt: Receipt Object from json
        """
        endpoint = f"{self.__endpoint.format(shop_id=shop_id)}/{receipt_id}/tracking"
        
        data = {
            "tracking_code":tracking_number, "carrier_name":carrier_name,
            "send_bcc":send_bcc, "note_to_buyer":note_to_buyer
        }
        
        json = self.auth.request(endpoint=endpoint, method="POST", data=data)
        return Receipt(**json)