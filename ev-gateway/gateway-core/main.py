
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

meter_data= []

class MeterReading(BaseModel):
    charger_ip: str
    timestamp :str
    energy_kwh: float

@app.post("/meter")
def receive_meter(data :MeterReading):
    meter_data.append(data)
    return {"status ": "received"}

def get_meters():
    return meter_data
    


@app.get("/meters", response_model=List[MeterReading])
def get_meters():
    return meter_data
