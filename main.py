from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import firebase_admin
from firebase_admin import credentials, auth
from typing import Optional
import os
from dotenv import load_dotenv
from sqlalchemy.future import select
from lib.db import get_db
from models.autocomplete import Autocomplete
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

load_dotenv()

firebase_type = os.getenv("FIREBASE_TYPE")
firebase_project_id = os.getenv("FIREBASE_PROJECT_ID")
firebase_private_key_id = os.getenv("FIREBASE_PRIVATE_KEY_ID")
firebase_private_key = os.getenv("FIREBASE_PRIVATE_KEY")
firebase_client_email = os.getenv("FIREBASE_CLIENT_EMAIL")
firebase_client_id = os.getenv("FIREBASE_CLIENT_ID")
firebase_auth_uri = os.getenv("FIREBASE_AUTH_URI")
firebase_token_uri = os.getenv("FIREBASE_TOKEN_URI")
firebase_auth_provider_x509_cert_url = os.getenv("FIREBASE_AUTH_PROVIDER_X509_CERT_URL")
firebase_client_x509_cert_url = os.getenv("FIREBASE_CLIENT_X509_CERT_URL")
firebase_universe_domain = os.getenv("FIREBASE_UNIVERSE_DOMAIN")

try:
    if all(
        [
            firebase_type,
            firebase_project_id,
            firebase_private_key_id,
            firebase_private_key,
            firebase_client_email,
        ]
    ):
        service_account_info = {
            "type": firebase_type,
            "project_id": firebase_project_id,
            "private_key_id": firebase_private_key_id,
            "private_key": firebase_private_key.replace("\\n", "\n"),
            "client_email": firebase_client_email,
            "client_id": firebase_client_id,
            "auth_uri": firebase_auth_uri,
            "token_uri": firebase_token_uri,
            "auth_provider_x509_cert_url": firebase_auth_provider_x509_cert_url,
            "client_x509_cert_url": firebase_client_x509_cert_url,
            "universe_domain": firebase_universe_domain,
        }
        cred = credentials.Certificate(service_account_info)
    else:
        cred = credentials.ApplicationDefault()

    firebase_admin.initialize_app(cred)
except Exception as e:
    print(f"Warning: Firebase Admin SDK initialization failed: {e}")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def verify_firebase_token(authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    try:
        if not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Invalid authorization format")

        token = authorization.split("Bearer ")[1]

        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")


@app.get("/")
def hello():
    return {"message": "Hello, World!"}


@app.get("/autocomplete")
async def autocomplete(
    query: str,
    limit: int = 5,
    user: dict = Depends(verify_firebase_token),
    db: AsyncSession = Depends(get_db)
):
    q = query.lower()
    stmt = select(Autocomplete).where(Autocomplete.text.ilike(f"{q}%")).limit(limit)
    result = await db.execute(stmt)
    starts_with = [row.text for row in result.scalars().all()]

    return {"suggestions": starts_with}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
