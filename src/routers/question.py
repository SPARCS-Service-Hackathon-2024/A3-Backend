from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from database import get_db
from models import LQuestions, LAnswers, LUsers
from pydantic import BaseModel
from routers.auth import get_current_user
from gpt.utils import generate_response

router = APIRouter()

@router.get("/{id}",
            summary="id로 질문 가져오기")
async def get_question(id: int, db: Session = Depends(get_db)):
    question = db.query(LQuestions).filter(
        LQuestions.question_id == id).first()
    if question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return {'id': question.question_id, 'content': question.content, 
            'is_answerable': question.is_answerable, 'next_question_id': question.next_question_id}

class ContentData(BaseModel):
    content: str

MAX_FOLLOWED_QUESTION = 4

@router.post("/{id}",
             summary="질문에 답변하기")
async def submit_answer(id: int, content: ContentData, user=Depends(get_current_user), db: Session = Depends(get_db)):
    question = db.query(LQuestions).filter(LQuestions.question_id == id).first()
    if not question.is_answerable:
        raise HTTPException(status_code=400, detail="답변할 수 없는 질문입니다.")
    if question.user_id != user.user_id and question.user_id != -1:
        raise HTTPException(status_code=403, detail="질문에 답변할 수 없습니다.")
    
    user = db.query(LUsers).filter(LUsers.user_id == user.user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # set user last question id
    
    answer = LAnswers(user_id=user.user_id, question_id=id, content=content.content)
    db.add(answer)
    db.commit()
    db.refresh(answer)

    result = await make_followed_question(id, db, user.user_id)

    if result['status'] == 'success':
        user.last_answered_question_id = result['id']
        db.commit()
        return {
            'question_id': result['id'],
        }
    else:
        user.last_answered_question_id = question.next_question_id
        db.commit()
        return {
            'question_id': question.next_question_id
        }

async def make_followed_question(parent_id: int, db: Session, user_id: int):
    parent = db.query(LQuestions).filter(LQuestions.question_id == parent_id).first()
    if parent.level == MAX_FOLLOWED_QUESTION:
        return {
            'status': 'fail',
            'message': '최대 꼬리질문 개수를 초과했습니다.'
        }
    context = make_context(parent=parent, db=db, user_id=user_id)
    print(context)
    contents = generate_response(context) #여기에 ai로 새 꼬리질문 만들어 넣기
    print(contents)
    for content in contents:
        if content == contents[-1]:
            is_answerable = True
        else:
            is_answerable = False
        followed = LQuestions(user_id=user_id, parents_id=parent_id, content=content, is_answerable=is_answerable, level=parent.level+1, chapter_id=parent.chapter_id, next_question_id=parent.next_question_id)
        db.add(followed)
        db.commit()
        db.refresh(followed)
    return {
        'status': 'success',
        'id': followed.question_id,
        'content': followed.content
    }

@router.get("/{id}/skip")
async def skip_question(id: int, user=Depends(get_current_user), db: Session = Depends(get_db)):
    question = db.query(LQuestions).filter(LQuestions.question_id == id).first()

    if question.user_id != user.user_id and question.user_id != -1:
        raise HTTPException(status_code=403, detail="질문을 스킵할 수 없습니다.")
    
    user = db.query(LUsers).filter(LUsers.user_id == user.user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.last_answered_question_id = question.next_question_id
    db.commit()
    
    return {
        'question_id': question.next_question_id
    }


def make_context(parent: LQuestions, db: Session, user_id: int):
    context = []
    p = parent
    while p is not None:
        print(p.content)
        a = db.query(LAnswers).filter(LAnswers.question_id == p.question_id).filter(LAnswers.user_id == user_id).first()
        print(a)
        print(a.content)
        if a is None:
            p = db.query(LQuestions).filter(LQuestions.question_id == p.parents_id).first()
            continue
        context.append(
            {
                'speaker': 'user',
                'text': a.content
            }
        )
        context.append(
            {
                'speaker': 'ai',
                'text': p.content
            }
        )
        p = db.query(LQuestions).filter(LQuestions.question_id == p.parents_id).first()
    context.reverse()
    return context