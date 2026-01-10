from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from ..services.auth_service import decode_token

security = HTTPBearer()

async def get_token_claims(auth: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    return decode_token(auth.credentials)
