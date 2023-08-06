from __future__ import annotations
from typing import Optional
from pydantic import BaseModel

class Review(BaseModel):
    shop_id: int
    listing_id: int
    transaction_id: Optional[int]
    buyer_user_id: Optional[int]
    rating: int
    review: Optional[str]
    language: str
    image_url_fullxfull: Optional[str]
    create_timestamp: int
    update_timestamp: int
    