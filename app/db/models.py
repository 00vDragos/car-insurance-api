from sqlalchemy import ForeignKey, String, Integer, Date, Text, Numeric, TIMESTAMP, func,DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column,relationship
from datetime import date,datetime

#Baza comuna pentru toate modelele:
class Base(DeclarativeBase):
    pass
#Tabela OWNER:
class Owner(Base):
    __tablename__ = 'owner'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]=mapped_column(String,nullable=False)
    email: Mapped[str]=mapped_column(String,nullable=False)
#Relatia 1-to-many (un propietar poate avea o lista cu masini:
    cars:Mapped[list["Car"]]=relationship("Car", back_populates="owner")

#Tabela Car, pentru masini
class Car(Base):
    __tablename__ = 'car' #numele tabelei
    id: Mapped[int] = mapped_column(primary_key=True) #id-ul masinii
    vin: Mapped[int] = mapped_column(String,nullable=False,unique=True) #seria de sasiu
    makeby: Mapped[str] = mapped_column(String,nullable=False) #marca masinii
    model: Mapped[str] = mapped_column(String,nullable=False) #modelul marcii
    year: Mapped[int | None] = mapped_column(Integer) #anul de fabricatie
    owner_id:Mapped[int]=mapped_column(ForeignKey('owner.id'),nullable=False) #

    owner: Mapped["Owner"] = relationship("Owner", back_populates="cars")
    policies: Mapped[list["InsurancePolicy"]] = relationship("InsurancePolicy", back_populates="car")
    claims: Mapped[list["Claim"]] = relationship("Claim", back_populates="car")

class InsurancePolicy(Base):
    __tablename__ = 'insurance_policy'
    id: Mapped[int] = mapped_column(primary_key=True)
    car_id: Mapped[int] = mapped_column(ForeignKey('car.id'),nullable=False)
    provider: Mapped[str] = mapped_column(String,nullable=False)
    start_date: Mapped[date] = mapped_column(Date,nullable=False)
    end_date: Mapped[date] = mapped_column(Date,nullable=False)
    logged_expiry_at = mapped_column(DateTime, nullable=True)

    car: Mapped["Car"] = relationship("Car", back_populates="policies")

class Claim(Base):
    __tablename__ = 'claim'

    id: Mapped[int] = mapped_column(primary_key=True)
    car_id: Mapped[int] = mapped_column(ForeignKey('car.id'),nullable=False)
    claim_date: Mapped[date] = mapped_column(Date,nullable=False)
    description: Mapped[str] = mapped_column(String,nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP,nullable=False, server_default=func.now())

    car:Mapped["Car"] = relationship("Car", back_populates="claims")


