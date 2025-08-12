# pco_tools/api/auth.py
import os
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

# Load .env from project root if present (non-overriding for precedence with system env vars)
load_dotenv(override=False)

def get_auth():
    app_id = os.environ.get("PCO_APPLICATION_ID")
    secret = os.environ.get("PCO_SECRET")
    if not app_id or not secret:
        raise ValueError("PCO_APPLICATION_ID and PCO_SECRET must be set in environment variables or .env file.")
    return HTTPBasicAuth(app_id, secret)

def get_headers():
    return {"Content-Type": "application/json"}
