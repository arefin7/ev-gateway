from pymodbus.client import ModbusTcpClient
import time
import json
import requests
from datetime import datetime
'''
CHARGER_IPS = [
    "192.168.1.101",
    "192.168.1.102"
]'''

CHARGER_IPS = [
    "modbus-sim"
]


MODBUS_PORT = 502
ENERGY_REGISTER = 0
UNIT_ID = 1

GATEWAY_URL = "http://gateway-core:8000/meter"

def read_energy(ip):
    client = ModbusTcpClient(ip, port=MODBUS_PORT)
    if not client.connect():
        print(f"Cannot connect to {ip}")
        return None

    result = client.read_holding_registers(
        address=ENERGY_REGISTER,
        count=2,
        unit=UNIT_ID
    )

    client.close()

    if result.isError():
        return None

    # Example: combine 2 registers (32-bit)
    energy = (result.registers[0] << 16) + result.registers[1]
    return energy / 1000.0  # if scaling needed


while True:
    for ip in CHARGER_IPS:
        energy = read_energy(ip)

        if energy is not None:
            payload = {
                "charger_ip": ip,
                "timestamp": datetime.utcnow().isoformat(),
                "energy_kwh": energy
            }

            print(json.dumps(payload))

            try:
                requests.post(GATEWAY_URL, json=payload)
            except:
                print("Gateway unreachable")

    time.sleep(10)
