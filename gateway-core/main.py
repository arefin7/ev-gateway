from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.exc import OperationalError
from database import engine, SessionLocal, Base
from models import MeterReadingDB
from typing import List
from sqlalchemy import text
from sqlalchemy.orm import Session
import time

app = FastAPI()


class MeterReading(BaseModel):
    charger_ip: str
    timestamp: str
    energy_kwh: float

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/meter")
def receive_meter(data: MeterReading, db: Session = Depends(get_db)):
    reading = MeterReadingDB(
        charger_ip=data.charger_ip,
        timestamp=data.timestamp,
        energy_kwh=data.energy_kwh
    )
    db.add(reading)
    db.commit()
    db.refresh(reading)
    return {"status": "stored in db"}

@app.get("/meters", response_model=List[MeterReading])
def get_meters(db: Session = Depends(get_db)):
    readings = db.query(MeterReadingDB).all()
    return readings

@app.on_event("startup")
def startup():
    retries = 10

    while retries > 0:
        try:
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            print("Database is ready")
            break
        except Exception as e:
            print("Database not ready, retrying...", e)
            retries -= 1
            time.sleep(3)

    if retries == 0:
        raise Exception("Could not connect to database")

    # Create tables AFTER successful connection
    Base.metadata.create_all(bind=engine)
