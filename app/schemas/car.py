from typing import Optional
from pydantic import BaseModel, Field
from app.schemas.owner import OwnerResponse

     # Create
class OwnerCreate(BaseModel):
    name: str
    email: Optional[str] = None


class CarCreate(BaseModel):
    vin: str
    makeby: str
    model: str
    year: int
    owner: OwnerCreate  # 🔁 Proprietar inclus direct în request

    #Response

class CarResponse(BaseModel):
    id: int
    vin: str
    makeby: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    owner: OwnerResponse

    class Config:
        from_attributes = True



