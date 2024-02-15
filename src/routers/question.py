from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from database import get_db
from models import LQuestions

router = APIRouter()

@router.get("/")
async def get_question(id: int, db: Session = Depends(get_db)):
    question = db.query(LQuestions).filter(LQuestions.question_id == id).first()
    
    if question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return {'id': question.question_id, 'content': question.content}