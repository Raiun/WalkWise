import os
import asyncio
import argparse
from dotenv import load_dotenv
from smartrent import async_login

load_dotenv()
email = os.getenv("EMAIL")
password = os.getenv("EMAIL_PASSWORD")

recognized_users = ["Test", "Test2"]

async def main():
    try:
        api = await async_login(email, password)
        locks = api.get_locks()
        first_lock = locks[0]

        if args.user in recognized_users:
            await first_lock.async_set_locked(False)
        else:
            print("Unrecognized User! DOOR WILL LOCK!")
            await first_lock.async_set_locked(True)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog="Unlock.py",
                    description="Unlock the door for recognized users")

    parser.add_argument("user", help="User passed from WalkWise neural network")

    args = parser.parse_args()
    print(args.user)
    
    asyncio.run(main())