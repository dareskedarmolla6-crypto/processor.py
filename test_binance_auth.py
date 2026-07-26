import os
import time
import hmac
import hashlib
import requests
from urllib.parse import urlencode
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("BINANCE_API_KEY")
secret = os.getenv("BINANCE_API_SECRET")

base = "https://api.binance.com"

params = {
    "timestamp": int(time.time() * 1000)
}

query = urlencode(params)

signature = hmac.new(
    secret.encode(),
    query.encode(),
    hashlib.sha256
).hexdigest()

url = f"{base}/api/v3/account?{query}&signature={signature}"

headers = {
    "X-MBX-APIKEY": api_key
}

response = requests.get(
    url,
    headers=headers,
    timeout=10
)

print("STATUS:", response.status_code)
print(response.text[:500])
