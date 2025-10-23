from datetime import date
from pydantic import BaseModel, Field, model_validator
from typing import Optional

class InsuranceValidityResponse(BaseModel):
    car_id: int
    date: date
    valid: bool

    class Config:
        from_attributes = True




class PolicyCreate(BaseModel):
    start_date: date = Field(..., alias="startDate")
    end_date: date = Field(..., alias="endDate")
    provider: Optional[str] = None

    class PolicyCreate(BaseModel):
        start_date: date = Field(..., alias="startDate")
        end_date: date = Field(..., alias="endDate")
        provider: Optional[str] = None

        @model_validator(mode="after")
        def check_dates(self) -> 'PolicyCreate':
            if self.end_date < self.start_date:
                raise ValueError("endDate must be after or equal to startDate")
            return self

        class Config:
            populate_by_name = True


class PolicyResponse(BaseModel):
    id: int
    car_id: int
    start_date: date
    end_date: date
    provider: Optional[str]
    logged_expiry_at: Optional[str] = None

    class Config:
        from_attributes = True