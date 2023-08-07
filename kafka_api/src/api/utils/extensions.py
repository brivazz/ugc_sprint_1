import json
import logging
from http import HTTPStatus

import jwt
import httpx
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer

from core.config import settings

bearer = HTTPBearer()


async def is_authenticated(token=Depends(bearer)):
    url = f"{settings.auth_server_url}/is_authenticated"
    headers = {"Authorization": f"Bearer {token.credentials}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        status_code = response.status_code
    if status_code == HTTPStatus.UNAUTHORIZED:
        raise HTTPException(status_code=401, detail="You are not authenticated")
    if status_code != HTTPStatus.OK:
        raise HTTPException(status_code=500, detail="Something was broke")

    token_inf = jwt.decode(
        token.credentials,
        options={
            "verify_signature": False
        }
    )
    return json.loads(token_inf['sub'])
