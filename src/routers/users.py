from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, Response, Request, status, HTTPException, Path
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from database import get_db
from models import LUsers

router = APIRouter(responses={404: {"description": "Not found"}})

# User 테이블에 있는 모든 사용자 조회


@router.get("/users", summary="모든 사용자 조회")
async def get_users(db: Session = Depends(get_db)):
    users = db.query(LUsers).all()
    return users
