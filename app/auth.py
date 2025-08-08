from fastapi import Header, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os

security = HTTPBearer()
EXPECTED_TOKEN = os.getenv("API_AUTH_TOKEN")  

def verify_token(auth: HTTPAuthorizationCredentials = Security(security)):
    if not EXPECTED_TOKEN:
        raise HTTPException(status_code=500, detail="Server misconfiguration: token not set.")

    if auth.scheme.lower() != "bearer" or auth.credentials != EXPECTED_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid or missing token.")
