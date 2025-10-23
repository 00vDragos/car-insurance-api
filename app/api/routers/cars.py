from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select

from app.db.session import SessionLocal
from app.db.models import Car
from app.schemas.car import CarResponse

router = APIRouter(
    prefix="/api/cars",
    tags=["Cars"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[CarResponse])
def get_all_cars(db: Session = Depends(get_db)):
    stmt = select(Car).options(selectinload(Car.owner))
    cars = db.execute(stmt).scalars().all()
    return cars
