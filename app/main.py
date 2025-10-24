from fastapi import FastAPI
from app.api.routers import cars_router, claims_router, policies_router
from app.api.routers import history_router
from app.core.scheduler import scheduler, check_expired_policies


app = FastAPI()
# Scheduler rulează doar în runtime local
scheduler.add_job(check_expired_policies, trigger="interval", minutes=10)
#check_expired_policies()
scheduler.start()

app.include_router(cars_router)
app.include_router(claims_router)
app.include_router(policies_router)
app.include_router(history_router)

@app.get("/health")
def health():
    return {"status": "ok"}
