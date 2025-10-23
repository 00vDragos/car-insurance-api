from datetime import date
from pydantic import BaseModel, Field, PositiveFloat


class ClaimCreate(BaseModel):
    claim_date: date = Field(..., alias="claimDate")
    description: str
    amount: PositiveFloat

    class Config:
        populate_by_name = True


class ClaimResponse(BaseModel):
    id: int
    claim_date: date
    description: str
    amount: float
    car_id: int

    class Config:
        from_attributes = True
