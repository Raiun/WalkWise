import asyncio
import os
from dotenv import load_dotenv
from smartrent import async_login

load_dotenv()
email = os.getenv("EMAIL")
password = os.getenv("EMAIL_PASSWORD")

async def main():
    try:
        api = await async_login(email, password)
        locks = api.get_locks()
        first_lock = locks[0]

        await first_lock.async_set_locked(False)
        await asyncio.sleep(10)
        await first_lock.async_set_locked(True)
    except Exception as e:
        print(e)

asyncio.run(main())