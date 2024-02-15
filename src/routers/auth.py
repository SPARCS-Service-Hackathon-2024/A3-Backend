from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from database import get_db
import requests
from models import LUsers

from pydantic import BaseModel, Field

router = APIRouter()

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

    if user is None:
        new_user = LUsers(kakao_id=user_info['id'], name=user_info['properties']['nickname'])
        db.add(new_user)
        db.commit()
        return new_user
    return user