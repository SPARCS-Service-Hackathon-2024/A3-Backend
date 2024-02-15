#  RUN ::
#  uvicorn main:app --reload
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import router, auth, question, chapter

app = FastAPI()

# 라우터 등록
app.include_router(router.router)
app.include_router(auth.router, prefix="/auth")
app.include_router(question.router, prefix="/question")
app.include_router

# CORS 설정
origins = [
    "http://localhost",
    "http://localhost:5173",
    "http://localhost:8000",
    "http://localhost:8080",
    "http://127.0.0.1:8000/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,  # allow cookie  (JWT)
    allow_methods=["*"],
    allow_headers=["*"],
)

# root
@app.get("/")
async def root():
    result = {"A3팀 화이팅!"}
    return result
