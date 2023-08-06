from dataclasses import dataclass

@dataclass
class EtsyRequestException(BaseException):
    status_code: int
    message: str
    
    def __repr__(self) -> str:
        return f"""
        \r{30*'-'}
        \rStatus Code: {self.status_code}
        \rError Message: {self.message}
    """
    
    def __str__(self) -> str:
        return f"""
        \r{30*'-'}
        \rStatus Code: {self.status_code}
        \rError Message: {self.message}
    """