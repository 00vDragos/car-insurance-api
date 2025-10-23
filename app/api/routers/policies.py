from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import date

from app.db.session import SessionLocal
from app.db.models import Car, InsurancePolicy
from app.schemas.policy import InsuranceValidityResponse,PolicyCreate, PolicyResponse


router = APIRouter(
    prefix="/api/cars",
    tags=["Policies"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/{car_id}/insurance-valid", response_model=InsuranceValidityResponse)
def check_insurance_validity(
    car_id: int,
    date: date = Query(..., description="Date to check"),
    db: Session = Depends(get_db)
):
    car = db.get(Car, car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")

    policy = db.execute(
        select(InsurancePolicy)
        .where(InsurancePolicy.car_id == car_id)
        .where(InsurancePolicy.start_date <= date)
        .where(InsurancePolicy.end_date >= date)
    ).scalar_one_or_none()

    return {
        "car_id": car_id,
        "date": date,
        "valid": policy is not None
    }



@router.post("/{car_id}/policies", response_model=PolicyResponse, status_code=201)
def create_policy_for_car(
    car_id: int,
    policy_in: PolicyCreate,
    db: Session = Depends(get_db)
):
    car = db.get(Car, car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")

    new_policy = InsurancePolicy(
        car_id=car.id,
        start_date=policy_in.start_date,
        end_date=policy_in.end_date,
        provider=policy_in.provider
    )

    db.add(new_policy)
    db.commit()
    db.refresh(new_policy)
    return new_policy