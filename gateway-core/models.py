from sqlalchemy import Column, Integer, String, Float
from database import Base

class MeterReadingDB(Base):
    __tablename__ = "meter_readings"

    id = Column(Integer, primary_key=True, index=True)
    charger_ip = Column(String, index=True)
    timestamp = Column(String)
    energy_kwh = Column(Float)
