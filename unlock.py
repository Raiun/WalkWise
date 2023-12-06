import os
import json
import asyncio
import argparse
import requests
from dotenv import load_dotenv
from smartrent import async_login

load_dotenv()
email = os.getenv("EMAIL")
password = os.getenv("EMAIL_PASSWORD")

async def main():
    valid_users = []
    url = "http://127.0.0.1:8000/authorizedUsers"
    response = requests.get(url)
    if response.status_code == 200:
        # Request was successful
        data = response.json()  # Assuming the response contains JSON data
        data = json.loads(data)
        print("Response data:", data)
        for i in range(len(data)):
            if data[i]["permitted"] == True:
                valid_users.append(data[i]["name"])
        print(f"Valid Users: {valid_users}")
    else:
        # Request failed
        print("Error:", response.status_code)
        print("Response content:", response.text)
    try:
        api = await async_login(email, password)
        locks = api.get_locks()
        first_lock = locks[0]

        if args.user in valid_users:
            #await first_lock.async_set_locked(False)
            status = "Unlock"
        else:
            print("Unrecognized User/user does not have permission! DOOR WILL LOCK!")
            #await first_lock.async_set_locked(True)
            status = "Lock"
        url = f"http://127.0.0.1:8000/addUnlock/{args.user}/{status}"
        response = requests.put(url)
        if response.status_code == 200:
            # Request was successful
            data = response.json()  # Assuming the response contains JSON data
            data = json.loads(data)
            print("Response data:", data)
        else:
            # Request failed
            print("Error:", response.status_code)
            print("Response content:", response.text)
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