import httpx
from ATRI.config import BotSelfConfig
from ATRI.log import logger as log


proxy = {"all://": BotSelfConfig.proxy} if BotSelfConfig.proxy else {}


async def get(url: str, **kwargs):
    log.debug(f"GET {url} by {proxy or 'No proxy'} | MORE: \n {kwargs}")
    async with httpx.AsyncClient(proxies=proxy) as client:  # type: ignore
        return await client.get(url, **kwargs)


async def post(url: str, **kwargs):
    log.debug(f"POST {url} by {proxy or 'No proxy'} | MORE: \n {kwargs}")
    async with httpx.AsyncClient(proxies=proxy) as client:  # type: ignore
        return await client.post(url, **kwargs)
