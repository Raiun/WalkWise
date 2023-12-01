import asyncio
from smartrent import async_login

async def main():
    try:
        api = await async_login('<EMAIL>', '<PASSWORD>')
        locks = api.get_locks()
        first_lock = locks[0]

        await first_lock.async_set_locked(False)
        await asyncio.sleep(10)
        await first_lock.async_set_locked(True)
    except Exception as e:
        print(e)

asyncio.run(main())