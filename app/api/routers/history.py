from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.session import SessionLocal
from app.db.models import Car, InsurancePolicy, Claim
from app.schemas.history import HistoryItem

router = APIRouter(
    prefix="/api/cars",
    tags=["History"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/{car_id}/history", response_model=list[HistoryItem])
def get_car_history(car_id: int, db: Session = Depends(get_db)):
    car = db.get(Car, car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")

    policies = db.execute(
        select(InsurancePolicy).where(InsurancePolicy.car_id == car_id)
    ).scalars().all()

    claims = db.execute(
        select(Claim).where(Claim.car_id == car_id)
    ).scalars().all()

    history = []

    for policy in policies:
        history.append(HistoryItem(
            type="POLICY",
            policyId=policy.id,
            startDate=policy.start_date,
            endDate=policy.end_date,
            provider=policy.provider
        ))

    for claim in claims:
        history.append(HistoryItem(
            type="CLAIM",
            claimId=claim.id,
            claimDate=claim.claim_date,
            amount=claim.amount,
            description=claim.description
        ))

    # Ordonare cronologică după data relevantă (startDate/claimDate)
    history.sort(key=lambda item: item.startDate or item.claimDate)

    return history
