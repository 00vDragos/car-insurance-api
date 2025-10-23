from typing import Optional
from pydantic import BaseModel
from app.schemas.owner import OwnerResponse


class CarResponse(BaseModel):
    id: int
    vin: str
    makeby: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    owner: OwnerResponse

    class Config:
        from_attributes = True
