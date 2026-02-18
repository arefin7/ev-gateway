from pymodbus.server.sync import StartTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
import threading
import time

energy_value = 6553700  # scaled value (kWh * 1000)

class EnergyDataBlock(ModbusSequentialDataBlock):

    def getValues(self, address, count=1):
        global energy_value

        # Return 2 registers (32-bit split)
        return [
            (energy_value >> 16) & 0xFFFF,
            energy_value & 0xFFFF
        ]


store = ModbusSlaveContext(
    hr=EnergyDataBlock(0, [0]*100)
)

context = ModbusServerContext(slaves=store, single=True)


def simulate_energy():
    global energy_value
    while True:
        energy_value += 500   # +0.5 kWh every 5 seconds
        time.sleep(5)


threading.Thread(target=simulate_energy, daemon=True).start()

print("Starting Modbus TCP server on port 502...")
StartTcpServer(context, address=("0.0.0.0", 502))

