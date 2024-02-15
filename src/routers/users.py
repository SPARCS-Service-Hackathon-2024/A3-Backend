from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, Response, Request, status, HTTPException, Path, Body
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from database import get_db
from models import LUsers

router = APIRouter(responses={404: {"description": "Not found"}})

# User 테이블에 있는 모든 사용자 조회


@router.get("/", summary="모든 사용자 조회")
async def get_users(db: Session = Depends(get_db)):
    users = db.query(LUsers).all()
    return users

# 수정할 사용자 정보


class UserUpdate(BaseModel):
    call: str = Field(..., title="사용자 전화번호", description="사용자 전화번호")
    address: str = Field(..., title="사용자 주소", description="사용자 주소")

# 사용자 정보 수정


@router.patch("/{user_id}", summary="사용자 정보 수정")
async def update_user(user_id: int = Path(..., title="사용자 ID", description="사용자 ID", ge=1),
                      user_update: UserUpdate = Body(..., title="사용자 정보",
                                              description="사용자 정보"),
                      db: Session = Depends(get_db)):
    user = db.query(LUsers).filter(LUsers.user_id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
    user.call = user_update.call
    user.address = user_update.address
    db.commit()
    return user
