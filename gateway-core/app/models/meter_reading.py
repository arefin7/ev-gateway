#app/models/meter_reading.py
from sqlalchemy import DateTime
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class MeterReadingDB(Base):
	__tablename__="meter_readings"

	id = Column(Integer, primary_key= True, index= True)
	charger_ip = Column(String,index = True, nullable =False)
	timestamp = Column(DateTime, default=datetime.utcnow)
	energy_kwh =Column(Float, nullable =False)
