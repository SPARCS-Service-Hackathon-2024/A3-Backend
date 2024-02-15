from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime, Text, text
from sqlalchemy.dialects.mysql import BIGINT, DATETIME, DATE, INTEGER
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class LUsers(Base):
    __tablename__ = 'LUsers'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=True)
    birthday = Column(DateTime, nullable=True)
    call = Column(String(255), nullable=True)
    address = Column(String(255), nullable=True)
    created_at = Column(DATETIME(fsp=3), nullable=False, server_default=text("CURRENT_TIMESTAMP(3)"))
    kakao_id = Column(BIGINT, nullable=True)
    last_answered_question_id = Column(Integer, nullable=True, default=1)
1
class LChapter(Base):
    __tablename__ = 'LChapter'
    chapter_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)

class LQuestions(Base):
    __tablename__ = 'LQuestions'
    question_id = Column(Integer, primary_key=True, autoincrement=True)
    is_fixed = Column(Boolean, nullable=False, default=False)
    chapter_id = Column(Integer, ForeignKey('LChapter.chapter_id', onupdate='Cascade'), nullable=False)
    user_id = Column(Integer, ForeignKey('LUsers.user_id', onupdate='Cascade'), nullable=False)
    parents_id = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DATETIME(fsp=3), nullable=False, server_default=text("CURRENT_TIMESTAMP(3)"))
    is_answerable = Column(Boolean, nullable=False, default=True)
    next_question_id = Column(Integer, nullable=True)
    level = Column(Integer, nullable=False, default=0)
                           
    LUsers = relationship('LUsers')
    LChapter = relationship('LChapter')

class LAnswers(Base):
    __tablename__ = 'LAnswers'
    answer_id = Column(Integer, primary_key=True, autoincrement=True)
    question_id = Column(Integer, ForeignKey('LQuestions.question_id', onupdate='Cascade'), nullable=False)
    user_id = Column(Integer, ForeignKey('LUsers.user_id', onupdate='Cascade'), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DATETIME(fsp=3), nullable=False, server_default=text("CURRENT_TIMESTAMP(3)"))

    question = relationship('LQuestions')
    user = relationship('LUsers')

class LSound(Base):
    __tablename__ = 'LSound'
    sound_id = Column(Integer, primary_key=True, autoincrement=True)
    question_id = Column(Integer, ForeignKey('LQuestions.question_id', onupdate='Cascade'), nullable=False)
    sound_url = Column(String(255), nullable=False)

    question = relationship("LQuestions")

class LImages(Base):
    __tablename__ = 'LImages'
    image_id = Column(Integer, primary_key=True, autoincrement=True)
    answer_id = Column(Integer, ForeignKey('LAnswers.answer_id', onupdate='Cascade'), nullable=False)
    image_url = Column(String(255), nullable=False)

    answer = relationship("LAnswers")


class LSummary(Base):
    __tablename__ = 'LSummary'
    summary_id = Column(Integer, primary_key=True, autoincrement=True)
    question_id = Column(Integer, ForeignKey('LQuestions.question_id', onupdate='Cascade'), nullable=False)
    user_id = Column(Integer, ForeignKey('LUsers.user_id', onupdate='Cascade'), nullable=False)
    chapter_id = Column(Integer, ForeignKey('LChapter.chapter_id', onupdate='Cascade'), nullable=False)
    content = Column(Text, nullable=False)

    question = relationship("LQuestions")
    user = relationship("LUsers")
    chapter = relationship("LChapter")