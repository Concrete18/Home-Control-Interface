import asyncio
from kasa import Discover, SmartPlug


devices = asyncio.run(Discover.discover())
if len(devices) == 0:
    print('No devices found.')
    exit()
else:
    for addr, dev in devices.items():
        asyncio.run(dev.update())
        print(f"{addr} >> {dev}")


async def main():
    p = SmartPlug("127.0.0.1")

    await p.update()
    print(p.alias)

    await p.turn_off()


if __name__ == "__main__":
    asyncio.run(main())
