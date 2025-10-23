from apscheduler.schedulers.background import BackgroundScheduler
from datetime import date, datetime
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.db.session import SessionLocal
from app.db.models import InsurancePolicy

scheduler = BackgroundScheduler()

def check_expired_policies():
    today = date.today()

    db: Session = SessionLocal()
    try:
        # Selectăm polițele care au expirat azi și nu au fost logate încă
        policies = db.execute(
            select(InsurancePolicy)
            .where(InsurancePolicy.end_date == today)
            .where(InsurancePolicy.logged_expiry_at == None)
        ).scalars().all()

        for policy in policies:
            print(f"📢 Policy {policy.id} for car {policy.car_id} expired on {policy.end_date}")
            policy.logged_expiry_at = datetime.utcnow()
            db.add(policy)

        if policies:
            db.commit()

    finally:
        db.close()
