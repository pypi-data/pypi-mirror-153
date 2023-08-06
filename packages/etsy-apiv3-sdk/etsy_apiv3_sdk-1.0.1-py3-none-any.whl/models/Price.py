from pydantic import BaseModel

class Price(BaseModel):
    amount: int
    divisor: int
    currency_code: str