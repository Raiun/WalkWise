# Records data from IMU for some time interval
# Writes to text file in format ax,ay,az,gx,gy,gz for each line

import asyncio
import struct
from bleak import BleakScanner, BleakClient

arduinoName = "Nate's Nano"
arduinoUUID = "722253D8-3943-7814-D96F-57266EF0DF11"
axID = "00002101-0000-1000-8000-00805f9b34fb"
ayID = "00002102-0000-1000-8000-00805f9b34fb"
azID = "00002103-0000-1000-8000-00805f9b34fb"
gxID = "00002744-0000-1000-8000-00805f9b34fb"
gyID = "00002745-0000-1000-8000-00805f9b34fb"
gzID = "00002746-0000-1000-8000-00805f9b34fb"

ax_data = []
ay_data = []
az_data = []
gx_data = []
gy_data = []
gz_data = []


def ax_callback(handle, data):
    [ax] = struct.unpack('f',data)
    ax_data.append(ax)

def ay_callback(handle, data):
    [ay] = struct.unpack('f',data)
    ay_data.append(ay)

def az_callback(handle, data):
    [az] = struct.unpack('f',data)
    az_data.append(az)

def gx_callback(handle, data):
    [gx] = struct.unpack('f',data)
    gx_data.append(gx)

def gy_callback(handle, data):
    [gy] = struct.unpack('f',data)
    gy_data.append(gy)

def gz_callback(handle, data):
    [gz] = struct.unpack('f',data)
    gz_data.append(gz)

async def collect_data(deviceName, fileName, collectionTime):
    async with BleakClient(await BleakScanner.find_device_by_name(deviceName)) as client:
        print(client.is_connected)
        await client.start_notify(axID, ax_callback)
        await client.start_notify(ayID, ay_callback)
        await client.start_notify(azID, az_callback)
        await client.start_notify(gxID, gx_callback)
        await client.start_notify(gyID, gy_callback)
        await client.start_notify(gzID, gz_callback)
        await asyncio.sleep(collectionTime)
        await client.stop_notify(axID)
        await client.stop_notify(ayID)
        await client.stop_notify(azID)
        await client.stop_notify(gxID)
        await client.stop_notify(gyID)
        await client.stop_notify(gzID)
        with open(fileName, 'w') as f:
            for i in range(min(len(ax_data), len(ay_data), len(az_data), len(gx_data), len(gy_data), len(gz_data))):
                ax = ax_data[i]
                ay = ay_data[i]
                az = az_data[i]
                gx = gx_data[i]
                gy = gy_data[i]
                gz = gz_data[i]
                line = str(ax) + "," + str(ay) + "," + str(az) + "," + str(gx) + "," + str(gy) + "," + str(gz)
                f.write(line)
                f.write('\n')
        f.close()

# async def main():
#     await collect_data(arduinoName,"hersh_10.txt",10)

# asyncio.run(main())