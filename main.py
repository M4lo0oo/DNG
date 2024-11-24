import requests
import random
import string
from concurrent.futures import ThreadPoolExecutor
from threading import Lock, Event

session = requests.Session()
file_lock = Lock()
stop_event = Event()

def generate_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))

def check_code_validity(code):
    url = f"https://discordapp.com/api/v9/entitlements/gift-codes/{code}?with_application=false&with_subscription_plan=true"
    response = session.get(url)
    return response.status_code == 200

def save_valid_code(code):
    with file_lock:
        with open("validcode.txt", "a") as file:
            file.write(f"{code}\n")

def process_code():
    if stop_event.is_set():
        return
    
    code = generate_code()
    if check_code_validity(code):
        print(f"\033[92mVALID\033[0m https://discord.gift/{code}")
        save_valid_code(code)
        stop_event.set()
    else:
        print(f"\033[91mINVALID\033[0m https://discord.gift/{code}")

with ThreadPoolExecutor(max_workers=10) as executor:
    while not stop_event.is_set():
        executor.submit(process_code)
