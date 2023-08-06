import json
import sys
import asyncio
import aiohttp

from pykostalpiko.Inverter import Piko


def main():
    asyncio.run(asnyc_main())


async def asnyc_main():
    async with aiohttp.ClientSession() as session:
        piko = Piko(session, sys.argv[1])
        data = await piko.async_fetch_all()

        print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
