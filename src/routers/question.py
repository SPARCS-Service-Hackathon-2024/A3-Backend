from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from database import get_db
from models import LQuestions

from routers.auth import get_current_user

router = APIRouter()


@router.get("/")
async def get_question(id: int, db: Session = Depends(get_db)):
    question = db.query(LQuestions).filter(
        LQuestions.question_id == id).first()

    if question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return {'id': question.question_id, 'content': question.content}


@router.get("/last",
            summary="마지막으로 답변한 질문의 id 가져오기")
async def get_last_question(user=Depends(get_current_user), db: Session = Depends(get_db)):
    question = db.query(LQuestions).filter(LQuestions.user_id == user.user_id).order_by(
        LQuestions.question_id.desc()).first()
    
    if question is None:
        return {'question_id': 1}
    return {'question_id': question.question_id, 'content': question.content}
