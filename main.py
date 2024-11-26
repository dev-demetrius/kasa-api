import json
from fastapi import FastAPI, HTTPException
from kasa import Discover, SmartPlug

app = FastAPI()

DEVICES_FILE = "devices.json"

@app.on_event("startup")
async def startup_event():
    try:
        with open(DEVICES_FILE, "x") as f:
            json.dump([], f)
    except FileExistsError:
        pass

@app.get("/discover")
async def discover_devices():
    devices = await Discover.discover()
    result = []

    for ip, device in devices.items():
        await device.update()
        result.append({
            "alias": device.alias,
            "ip": ip,
            "state": device.is_on,
            "brightness": getattr(device, "brightness", None),
            "rssi": device.rssi,
            "model": device.model,
            "mac": device.mac,
        })

    with open(DEVICES_FILE, "w") as f:
        json.dump(result, f, indent=4)

    return {"message": "Discovery completed", "devices": result}

@app.get("/devices")
def get_devices():
    try:
        with open(DEVICES_FILE, "r") as f:
            devices = json.load(f)
        return devices
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Devices file not found")

@app.post("/devices/{ip}/on")
async def turn_on_device(ip: str):
    try:
        plug = SmartPlug(ip)
        await plug.update()
        await plug.turn_on()
        return {"message": f"{plug.alias} turned on"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/devices/{ip}/off")
async def turn_off_device(ip: str):
    try:
        plug = SmartPlug(ip)
        await plug.update()
        await plug.turn_off()
        return {"message": f"{plug.alias} turned off"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
