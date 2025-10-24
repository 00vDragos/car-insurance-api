from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select

from app.db.session import SessionLocal
from app.db.models import Car, Owner
from app.schemas.car import CarResponse, CarCreate

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

@router.post("/", response_model=CarResponse, status_code=status.HTTP_201_CREATED)
def create_car(car_in: CarCreate, db: Session = Depends(get_db)):
    # Creează proprietarul
    owner = Owner(name=car_in.owner.name, email=car_in.owner.email)
    db.add(owner)
    db.flush()  # Primește ID-ul fără commit

    # Creează mașina
    car = Car(
        vin=car_in.vin,
        makeby=car_in.makeby,
        model=car_in.model,
        year=car_in.year,
        owner_id=owner.id
    )
    db.add(car)
    db.commit()
    db.refresh(car)
    return car