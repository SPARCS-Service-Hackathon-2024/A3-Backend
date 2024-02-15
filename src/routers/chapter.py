from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, Response, Request, status, HTTPException, Path
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from database import get_db
from models import LChapter

router = APIRouter(responses={404: {"description": "Not found"}})