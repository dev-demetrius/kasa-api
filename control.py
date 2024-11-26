import asyncio
from kasa import SmartPlug as Light

async def control_device(ip):
    light = Light(ip)
    await light.update()  # Get device state

    print(f"Device: {light.alias} is {'ON' if light.is_on else 'OFF'}")
    
    # usage data
    usage = light.modules.get("usage")  
    if usage:
        print(f"Minutes on this month: {usage.usage_this_month}")
        print(f"Minutes on today: {usage.usage_today}")
    else:
        print("Usage data not available for this device.")
    
    # Turn on or off the plug
    if not light.is_on:
        await light.turn_on()
        print("Turned on the light!")
    else:
        await light.turn_off()
        print("Turned off the light!")

if __name__ == "__main__":
    device_ip = ""  # device's IP
    asyncio.run(control_device(device_ip))
