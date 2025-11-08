import os
import base64
import requests
from datetime import datetime

MPESA_ENV = os.getenv("MPESA_ENV", "sandbox")
CONSUMER_KEY = os.getenv("MPESA_CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("MPESA_CONSUMER_SECRET")
SHORTCODE = os.getenv("MPESA_SHORTCODE")
PASSKEY = os.getenv("MPESA_PASSKEY")

BASE_URL = "https://sandbox.safaricom.co.ke" if MPESA_ENV == "sandbox" else "https://api.safaricom.co.ke"

def get_access_token():
    url = f"{BASE_URL}/oauth/v1/generate?grant_type=client_credentials"
    resp = requests.get(url, auth=(CONSUMER_KEY, CONSUMER_SECRET), timeout=10)
    resp.raise_for_status()
    return resp.json()["access_token"]

def mpesa_timestamp():
    return datetime.utcnow().strftime("%Y%m%d%H%M%S")

def generate_password(shortcode: str, passkey: str, timestamp: str):
    s = f"{shortcode}{passkey}{timestamp}"
    return base64.b64encode(s.encode()).decode()

def stk_push(phone: str, amount: int, account_ref: str, callback_url: str, description: str = "Payment"):
    token = get_access_token()
    timestamp = mpesa_timestamp()
    password = generate_password(SHORTCODE, PASSKEY, timestamp)
    url = f"{BASE_URL}/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    payload = {
        "BusinessShortCode": SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone,           # customer phone in format 2547XXXXXXXX
        "PartyB": SHORTCODE,
        "PhoneNumber": phone,
        "CallBackURL": callback_url,
        "AccountReference": account_ref,
        "TransactionDesc": description
    }
    resp = requests.post(url, json=payload, headers=headers, timeout=15)
    resp.raise_for_status()
    return resp.json()