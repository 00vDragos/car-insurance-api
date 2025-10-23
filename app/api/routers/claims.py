from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db.models import Car, Claim
from app.schemas.claim import ClaimCreate, ClaimResponse

router = APIRouter(
    prefix="/api/cars",
    tags=["Claims"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/{car_id}/claims", response_model=ClaimResponse, status_code=status.HTTP_201_CREATED)
def create_claim_for_car(car_id: int, claim_in: ClaimCreate, db: Session = Depends(get_db)):
    car = db.get(Car, car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")

    new_claim = Claim(
        car_id=car.id,
        claim_date=claim_in.claim_date,
        description=claim_in.description,
        amount=claim_in.amount
    )

    db.add(new_claim)
    db.commit()
    db.refresh(new_claim)
    return new_claim
