import os

from dotenv import load_dotenv
from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer
from jwt import encode, decode

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')


def create_token(data: dict) -> str:
    token: str = encode(payload=data, key=SECRET_KEY, algorithm="HS256")
    return token


def validate_token(token: str) -> dict:
    data: dict = decode(token, key=SECRET_KEY, algorithms=["HS256"])
    return data


class JwtBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data["email"] != "admin@gmail.com":
            raise HTTPException(status_code=401, detail="Credenciales inválidas")
