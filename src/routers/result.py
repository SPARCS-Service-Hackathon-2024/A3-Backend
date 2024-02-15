from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, Response, Request, status, HTTPException, Path
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from routers.auth import get_current_user

from database import get_db
from models import LSummary

router = APIRouter(responses={404: {"description": "Not found"}})

@router.get("", summary="모든 요약본 가져오기")
async def get_chapters(user=Depends(get_current_user), db: Session = Depends(get_db)):
    result = db.query(LSummary).all()
    print(result)
    return result