from typing import Optional
from pydantic import BaseModel


class OwnerResponse(BaseModel):
    id: int
    name: str
    email: Optional[str] = None

    class Config:
        from_attributes = True
