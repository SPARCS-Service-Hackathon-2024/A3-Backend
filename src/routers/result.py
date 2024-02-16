from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, Response, Request, status, HTTPException, Path
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from routers.auth import get_current_user

from database import get_db
from models import LSummary, LChapter, LQuestions

router = APIRouter(responses={404: {"description": "Not found"}})

@router.get("", summary="모든 요약본 가져오기")
async def get_chapters(user=Depends(get_current_user), db: Session = Depends(get_db)):
    summary_list = db.query(LSummary).filter(LSummary.user_id == user.user_id).all()
    result = []
    chapters = db.query(LChapter).all()
    for chapter in chapters:
        summary = list(filter(lambda x: x.chapter_id == chapter.chapter_id, summary_list))
        if summary:
            summaries = []
            for s in summary:
                summaries.append({
                    "summary_id": s.summary_id,
                    "question": db.query(LQuestions).filter(LQuestions.question_id == s.question_id).first().content,
                    "content": s.content,
                })
            result.append({
                "chapter_id": chapter.chapter_id,
                "chapter_title": chapter.title,
                "summaries": summaries
            })
    result = list(filter(lambda x: x["summaries"], result))
    result = sorted(result, key=lambda x: x["chapter_id"])
    return result