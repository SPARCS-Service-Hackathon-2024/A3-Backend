from fastapi import Header, Depends, APIRouter, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database import get_db
import requests
from models import LUsers
from datetime import datetime, timedelta


from jose import jwt, JWTError

SECRET_KEY = "secretkey"
ALGORITHM = "HS256"

from pydantic import BaseModel, Field

router = APIRouter()

class TokenData(BaseModel):
    id_token: str

async def get_current_user(token: str = Header(None), db: Session = Depends(get_db)):
    if token is None:
        raise HTTPException(status_code=401, detail="토큰이 필요합니다.")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        print(user_id)
        print(user_id)
        print(user_id)
        print(user_id)

        user_id: int = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다.1")
        if payload.get("exp") < datetime.utcnow():
            raise HTTPException(status_code=401, detail="만료된 토큰입니다.")
    except JWTError:
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다.2")

    user = db.query(LUsers).filter(LUsers.user_id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

    return user

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
    access_token = jwt.encode({"sub": user.user_id}, SECRET_KEY, algorithm=ALGORITHM)

    if user is None:
        new_user = LUsers(kakao_id=user_info['id'], name=user_info['properties']['nickname'])
        db.add(new_user)
        db.commit()
        new_user.access_token = access_token
        return new_user
    
    user.access_token = access_token
    return user

@router.get("/protected-route")
async def protected_route(current_user: LUsers = Depends(get_current_user)):
    return {"user": current_user.name, "message": "보호된 경로에 접근할 수 있습니다."}