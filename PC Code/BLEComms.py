import asyncio
from bleak import BleakClient
import struct
import matplotlib.pyplot as plt
import time

address = "AF:72:20:04:66:5F"
ACC_UUID = "917649A1-D98E-11E5-9EEC-0002A5D5C51B"
GYRO_UUID = "917649A2-D98E-11E5-9EEC-0002A5D5C51B"

acc_dat = []
gyro_dat = []

async def main():
    async with BleakClient(address) as client:
        while True:
            start = time.time()
            acc_data = await client.read_gatt_char(ACC_UUID)
            gyro_data = await client.read_gatt_char(GYRO_UUID)
            acc_data = struct.unpack('fff', acc_data)
            gyro_data = struct.unpack('fff', gyro_data)
            print("Gyro: ", end="")
            print(gyro_data)
            print("Acc: ", end="")
            print(acc_data)
            end = time.time()
            print("Update Freq: " + str(1/(end-start)))

asyncio.run(main())
