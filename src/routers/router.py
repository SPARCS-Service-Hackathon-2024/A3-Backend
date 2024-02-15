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

# User 테이블에 사용자 추가
# request: name, birthday, call, address
class UserRequest(BaseModel):
    name: str = Field(..., example="홍길동")
    birthday: datetime = Field(..., example="1998-11-18")
    call: str = Field(..., example="010-1234-5678")
    address: str = Field(..., example="서울시 강남구 역삼동")

@router.post("/users", summary="사용자 추가")
async def create_user(request: UserRequest, db: Session = Depends(get_db)):
    new_user = LUsers(name=request.namLe, birthday=request.birthday, call=request.call, address=request.address)
    db.add(new_user)
    db.commit()
    return {"message": "create user"}

"""





@router.get("/monthly/{day}", summary="이달의 일정 가져오기")
async def get_monthly_schedule(day: str = Path(...,example="2023-11-18"), db: Session = Depends(get_db)):
    # day 파싱해서 year, month 구하기
    year = day.split("-")[0]
    month = day.split("-")[1]
    # year, month로 일정 가져와서 List[EventResponse]로 반환
    events = db.query(K_Event).filter(K_Event.event_date.like(f"{year}-{month}-%")).all()
    return events


@router.get("/daily/{day}", summary="오늘의 일정 가져오기")
async def get_daily_schedule(day: str = Path(...,example="2023-11-18"), db: Session = Depends(get_db)):
    # day 파싱해서 year, month, day 구하기
    year = day.split("-")[0]
    month = day.split("-")[1]
    day = day.split("-")[2]
    # year, month, day로 일정 가져와서 List[EventResponse]로 반환
    events = db.query(K_Event).filter(K_Event.event_date == f"{year}-{month}-{day}").all()
    # priotiry 순으로 정렬
    events.sort(key=lambda x: x.priority, reverse=True)
    return events

# 지정 일정(designated event) 추가하기
# request: date, event_name
class DesignatedEventRequest(BaseModel):
    event_date: str = Field(..., example="2023-12-10")
    event_name: str = Field(..., example="수업")
    # 카테고리
    category: str = Field(..., example="기타")
    # 우선순위
    priority: int = Field(..., example=3)

@router.post("/designated", summary="지정 일정 추가")
async def create_designated_event(request: DesignatedEventRequest, db: Session = Depends(get_db)):
    new_event = K_Event(event_date=request.event_date, event_name=request.event_name, priority=request.priority, event_type="지정", category=request.category, finished=False, activated=False)
    db.add(new_event)
    db.commit()
    return {"message": "create designated event"}


# 고정 일정(fixed event) 추가하기
# request: event_name, weeks(요일들, 중복선택가능)
class FixedEventRequest(BaseModel):
    today: str = Field(..., example="2023-12-10")
    event_name: str = Field(..., example="수업")
    weeks: list = Field(..., example=["월", "수", "금"])

@router.post("/fixed", summary="고정 일정 추가")
async def create_fixed_event(request: FixedEventRequest, db: Session = Depends(get_db)):
    # 오늘부터 종강날짜까지의 모든 날짜 사이의 weeks에 있는 요일들에 일정 추가
    # 오늘 날짜 파싱해서 year, month, day 구하기
    year = request.today.split("-")[0]
    month = request.today.split("-")[1]
    day = request.today.split("-")[2]
    # 종강 날짜 파싱해서 year, month, day 구하기
    end_date = db.query(K_MainEvent).filter(K_MainEvent.main_event_id == 1).first()
    # end_date를 문자열로 바꿔서 파싱
    end_date = str(end_date.event_date)
    end_year = end_date.split("-")[0]
    end_month = end_date.split("-")[1]
    end_day = end_date.split("-")[2]
    # 오늘부터 종강날짜까지의 모든 날짜 사이의 weeks에 있는 요일들에 일정 추가
    # 오늘 날짜부터 종강날짜까지 모든 날짜 구하기
    # 오늘 날짜
    today = datetime(int(year), int(month), int(day))
    # 종강 날짜
    end_date = datetime(int(end_year), int(end_month), int(end_day))
    # 오늘부터 종강날짜까지 모든 날짜
    all_dates = []
    while today <= end_date:
        all_dates.append(today)
        today += timedelta(days=1)
    # weeks에 한글 요일들을 영어 요일로 바꾸기
    for i in range(len(request.weeks)):
        if request.weeks[i] == "월":
            request.weeks[i] = "Mon"
        elif request.weeks[i] == "화":
            request.weeks[i] = "Tue"
        elif request.weeks[i] == "수":
            request.weeks[i] = "Wed"
        elif request.weeks[i] == "목":
            request.weeks[i] = "Thu"
        elif request.weeks[i] == "금":
            request.weeks[i] = "Fri"
        elif request.weeks[i] == "토":
            request.weeks[i] = "Sat"
        elif request.weeks[i] == "일":
            request.weeks[i] = "Sun"
    # weeks에 있는 요일들에 일정 추가
    for date in all_dates:
        if date.strftime("%a") in request.weeks:
            new_event = K_Event(event_date=date, event_name=request.event_name, priority=0, event_type="고정", category="기타", finished=False, activated=False)
            db.add(new_event)
            db.commit()
    return {"message": "create fixed event"}
    # 나중에 로직 수정해줘야 함


# 루틴 일정(routine event) 추가하기
class RoutineEventRequest(BaseModel):
    today: str = Field(..., example="2023-12-17")
    event_name: str = Field(..., example="영어 회화 공부")
    have_to: int = Field(..., example=3)    # priority
    want_to: int = Field(..., example=5)

@router.post("/routine", summary="루틴 일정 추가")
async def create_routine_event(request: RoutineEventRequest, db: Session = Depends(get_db)):
    # 오늘부터 종강날짜까지의 모든 날짜에 일정 추가
    # 오늘 날짜 파싱해서 year, month, day 구하기
    year = request.today.split("-")[0]
    month = request.today.split("-")[1]
    day = request.today.split("-")[2]
    
    # 종강 날짜 파싱해서 year, month, day 구하기
    end_date = db.query(K_MainEvent).filter(K_MainEvent.main_event_id == 1).first()
    # end_date를 문자열로 바꿔서 파싱
    end_date = str(end_date.event_date)
    end_year = end_date.split("-")[0]
    end_month = end_date.split("-")[1]
    end_day = end_date.split("-")[2]
    # 오늘부터 종강날짜까지의 모든 날짜에 일정 추가
    # 오늘 날짜
    today = datetime(int(year), int(month), int(day))
    # 종강 날짜
    end_date = datetime(int(end_year), int(end_month), int(end_day))
    # 오늘부터 종강날짜까지 모든 날짜
    all_dates = []
    while today <= end_date:
        all_dates.append(today)
        today += timedelta(days=1)
    # 모든 날짜에 일정 추가
    for date in all_dates:
        new_event = K_Event(event_date=date, event_name=request.event_name, priority=request.have_to, event_type="루틴", category="기타", finished=False, activated=False)
        db.add(new_event)
        db.commit()
    return {"message": "create routine event"}



# 일정 수정하기
# event_id로 일정 찾아서 수정
@router.put("/event/{event_id}", summary="일정 수정")
async def update_event(event_id: int, request: EventResponse, db: Session = Depends(get_db)):
    event = db.query(K_Event).filter(K_Event.event_id == event_id).first()
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    event.event_date = request.event_date
    event.event_name = request.event_name
    event.priority = request.priority
    event.event_type = request.event_type
    event.category = request.category
    db.commit()
    return {"message": "update event"}


@router.get("/end-date", summary="종강 날짜 조회")
async def get_end_date(db: Session = Depends(get_db)):
    end_date = db.query(K_MainEvent).filter(K_MainEvent.main_event_id == 1).first()
    return end_date

# 종강 날짜 수정하기
# Request: {"end_date": "2021-08-31"}
class EndDateUpdateRequest(BaseModel):
    end_date: str = Field(..., example="2023-12-24")

@router.put("/end-date", summary="종강 날짜 수정")
async def update_end_date(request: EndDateUpdateRequest, db: Session = Depends(get_db)):
    end_date = db.query(K_MainEvent).filter(K_MainEvent.main_event_id == 1).first()
    if end_date is None:
        raise HTTPException(status_code=404, detail="Event not found")
    end_date.event_date = request.end_date
    db.commit()
    return {"message": "update end_date"}

# 고정 일정 조회
# event_type이 "고정"인 일정들 조회
@router.get("/fixed", summary="고정 일정 조회")
async def get_fixed_schedule(db: Session = Depends(get_db)):
    fixed_events = db.query(K_Event).filter(K_Event.event_type == "고정").all()
    return fixed_events

# 루틴 일정 조회
# event_type이 "루틴"인 일정들 조회
@router.get("/routine", summary="루틴 일정 조회")
async def get_routine_schedule(db: Session = Depends(get_db)):
    routine_events = db.query(K_Event).filter(K_Event.event_type == "루틴").all()
    return routine_events

# 지정 일정 조회
# event_type이 "지정"인 일정들 조회
@router.get("/designated", summary="지정 일정 조회")
async def get_designated_schedule(db: Session = Depends(get_db)):
    designated_events = db.query(K_Event).filter(K_Event.event_type == "지정").all()
    return designated_events


"""