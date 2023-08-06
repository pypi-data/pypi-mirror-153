import aiohttp
import asyncio

from pykostalpiko.dxs import Entries


class Piko:
    def __init__(self, client_session: aiohttp.ClientSession, host: str,  username: str = "pvserver", password: str = "pvwr"):
        """
        Piko Inverter Instance
        """
        self._host = host
        self._username = username
        self._password = password
        self._client_session = client_session
        self._data = {}

    async def _async_fetch(self, session: aiohttp.ClientSession, *entries: Entries) -> dict:
        """
        Fetch the data from the inverter

        Limited to 0 to 10 DXS entries
        """

        # Check amount of requested entries
        if (len(entries) == 0):
            raise Exception('No entries specified')
        elif (len(entries) > 10):
            raise Exception('Too many entries specified')

        def _build_param(dxs: Entries) -> str:
            return f'dxsEntries={dxs.value}'

        params = map(_build_param, entries)
        url = f'http://{self._host}/api/dxs.json?' + '&'.join(params)

        async with session.get(url) as response:
            json = await response.json(content_type='text/plain')
            return self.__format_response(json)

    async def async_fetch(self, *entries: Entries) -> dict:
        """
        Fetch the data from the inverter
        """

        # Spread the entries into groups of 10 to avoid too many dxsEntries
        entries_paged = [entries[i:i + 10]
                         for i in range(0, len(entries), 10)]
        # TODO: Do something with the response
        for req in asyncio.as_completed([self._async_fetch(self._client_session, *entries_page) for entries_page in entries_paged]):
            # Wait for the request to complete
            res = await req

            if res != None:
                # Combine existing data with newly fetched data
                self._data = {**self._data, **res}
        return self._data

    async def async_fetch_all(self) -> dict:
        """
        Fetch all available data from the inverter
        """
        return await self.async_fetch(*Entries)

    def __format_response(self, json) -> dict:
        if json == None:
            return None

        new = {}
        entries = json['dxsEntries']

        for entry in entries:
            new[Entries(entry['dxsId']).name] = entry['value']

        return new
