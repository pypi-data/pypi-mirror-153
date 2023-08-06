from fastapi import Depends, HTTPException, requests
from fastapi.security import HTTPBearer
from firebase_admin import auth
from starlette import status

jwtBearer = HTTPBearer()


def verify_and_decode_jwt(token: dict = Depends(jwtBearer)):
    try:
        user = auth.verify_id_token(token.credentials)
        org = user.get('o')
        role = user.get('r')
        requests.org = org
        requests.role = role
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid JWT",
        )


def verify_owner_and_get_id(token: dict = Depends(jwtBearer)):
    try:
        user = auth.verify_id_token(token.credentials)
        org = user.get('o')
        role = user.get('r')
        requests.owner = user.get('email')
        requests.org = org
        requests.role = role
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid JWT",
        )


def verify_and_get_jwt(token: dict = Depends(jwtBearer)):
    try:
        user = auth.verify_id_token(token.credentials)
        org = user.get('o')
        role = user.get('r')
        requests.org = org
        requests.role = role
        requests.token = token
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid JWT",
        )