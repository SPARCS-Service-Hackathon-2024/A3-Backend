#  RUN ::
#  uvicorn main:app --reload
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, question, chapter, users

app = FastAPI()

# 라우터 등록
app.include_router(users.router, prefix="/user", tags=["user"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(question.router, prefix="/question", tags=["question"])
app.include_router(chapter.router, prefix="/chapter", tags=["chapter"])

# CORS 설정
origins = [
    "http://localhost",
    "http://localhost:5173",
    "http://localhost:8000",
    "http://localhost:8080",
    "http://127.0.0.1:8000/",
    "https://life-book-tau.vercel.app",
    "https://life-book-tau.vercel.app/",
    "https://a3.r4bb1t.dev/",
    "https://a3.r4bb1t.dev"
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
