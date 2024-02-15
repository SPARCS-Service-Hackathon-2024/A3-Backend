from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from database import get_db
import requests
from models import LUsers
from datetime import datetime, timedelta

from jose import jwt
SECRET_KEY = "secretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

from pydantic import BaseModel, Field

router = APIRouter()

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
class TokenData(BaseModel):
    id_token: str

@router.post("/kakao")
async def kakao_login(token_data: TokenData, db: Session = Depends(get_db)):
    headers = {
        "Authorization": f"Bearer {token_data.id_token}"
    }
    response = requests.post("https://kapi.kakao.com/v2/user/me", headers=headers)
    if response.status_code == 200:
        user_info = response.json()
        print(user_info)
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch user information from Kakao")
    
    user = db.query(LUsers).filter(LUsers.kakao_id == user_info['id']).first()

    # access token 만들기
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.kakao_id}, expires_delta=access_token_expires
    )

    if user is None:
        new_user = LUsers(kakao_id=user_info['id'], name=user_info['properties']['nickname'])
        db.add(new_user)
        db.commit()
        new_user.access_token = access_token
        return new_user
    
    user.access_token = access_token
    return user