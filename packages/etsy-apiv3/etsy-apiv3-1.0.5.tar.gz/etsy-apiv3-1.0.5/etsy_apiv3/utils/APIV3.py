from dataclasses import dataclass
from typing import Callable
from requests_oauthlib import OAuth2Session
from etsy_apiv3.utils.RequestException import EtsyRequestException

def token_saver(token):
    return token

@dataclass(frozen=True)
class EtsyAuth:
    """
    A class to represent a etsy auth
    
    Attributes:
        headers (dict): Request Headers
        session (requests_oauthlib.OAuth2Session): Requests Oauthlib Object
    """
    
    headers: dict
    session: OAuth2Session
    __base_endpoint:str = "https://openapi.etsy.com/v3/application"
    
    def request(self, endpoint: str, method="GET", *args, **kwargs) -> dict:
        """ 
        Send Request to target endpoint by method
        
        Args:
            endpoint (str): Api Endpoint Url
            method (str, optional): HTTP Methods [GET, POST, PUT, DELETE, UPDATE]. Defaults to "GET".

        Raises:
            EtsyRequestException: EtsyRequestException(status_code, message)

        Returns:
            json: Json From Request Response
        """

        url = f"{self.__base_endpoint}/{endpoint}"
        req = self.session.request(method, url, headers=self.headers, *args, **kwargs)

        response: dict = req.json()
        if "error" in response.keys():
            raise EtsyRequestException(req.status_code, response["error"])
        return response



class EtsySession:
    
    def __init__(self, client_key: str, client_secret: str, token: dict, refresh_url="https://api.etsy.com/v3/public/oauth/token", token_updater: Callable = token_saver):
        self.CLIENT_KEY = client_key
        self.CLIENT_SECRET = client_secret
        self.TOKEN = token
        self.REFRESH_URL = refresh_url
        self.TOKEN_UPDATER = token_updater
        
    def create_auth(self):
        refresh_kwargs = {
            'client_id': self.CLIENT_KEY,
            'client_secret': self.CLIENT_SECRET,
        }
        
        headers = {"x-api-key": self.CLIENT_KEY}
        session = OAuth2Session(client_id=self.CLIENT_KEY, token=self.TOKEN, auto_refresh_kwargs=refresh_kwargs, auto_refresh_url=self.REFRESH_URL, token_updater=self.TOKEN_UPDATER)
        
        return EtsyAuth(headers=headers, session=session)
        
