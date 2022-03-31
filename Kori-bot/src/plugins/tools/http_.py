import httpx

async def get_url(url: str,timeout_: int):
    async with httpx.AsyncClient() as client:
        res = await client.get(url,timeout=timeout_)
        return res.text
        
async def post_url(url: str,timeout_: int):
    async with httpx.AsyncClient() as client:
        res = await client.post(url,timeout=timeout_)
        print(res.text)
        return res.text