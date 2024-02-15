from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from database import get_db
import requests
from models import LUsers

router = APIRouter()

@router.post("/kakao")
async def kakao_login(id_token: str, db: Session = Depends(get_db)):
    headers = {
        "Authorization": f"Bearer {id_token}"
    }
    response = requests.post("https://kapi.kakao.com/v2/user/me", headers=headers)
    if response.status_code == 200:
        user_info = response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch user information from Kakao")
    
    user = db.query(LUsers).filter(LUsers.kakao_id == user_info['id']).first()

    if user is None:
        new_user = LUsers(kakao_id=user_info['id'], username=user_info['properties']['username'], email=user_info['kakao_account']['email'])
        print(new_user)
        db.add(new_user)
        db.commit()
        return new_user
    print(user)
    return user