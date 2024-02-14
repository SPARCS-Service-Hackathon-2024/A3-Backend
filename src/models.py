from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime, Text, text
from sqlalchemy.dialects.mysql import BIGINT, DATETIME, DATE, INTEGER
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Users(Base):
    __tablename__ = 'Users'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=True)
    birthday = Column(DateTime, nullable=True)
    call = Column(String(255), nullable=True)
    address = Column(String(255), nullable=True)
    created_at = Column(DATETIME(fsp=3), nullable=False, server_default=text("CURRENT_TIMESTAMP(3)"))

    questions = relationship("Questions", back_populates="user")
    answers = relationship("Answers", back_populates="user")

class Questions(Base):
    __tablename__ = 'Questions'
    question_id = Column(Integer, primary_key=True, autoincrement=True)
    is_fixed = Column(Boolean, nullable=False, default=False)
    user_id = Column(Integer, ForeignKey('Users.user_id', onupdate='Cascade'), nullable=False)
    parents_id = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DATETIME(fsp=3), nullable=False, server_default=text("CURRENT_TIMESTAMP(3)"))

    user = relationship("Users", back_populates="questions")
    answers = relationship("Answers", back_populates="question")
    sounds = relationship("Sound", back_populates="question")

class Answers(Base):
    __tablename__ = 'Answers'
    answer_id = Column(Integer, primary_key=True, autoincrement=True)
    question_id = Column(Integer, ForeignKey('Questions.question_id', onupdate='Cascade'), nullable=False)
    user_id = Column(Integer, ForeignKey('Users.user_id', onupdate='Cascade'), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DATETIME(fsp=3), nullable=False, server_default=text("CURRENT_TIMESTAMP(3)"))

    question = relationship("Questions", back_populates="answers")
    user = relationship("Users", back_populates="answers")
    images = relationship("Images", back_populates="answer")

class Sound(Base):
    __tablename__ = 'Sound'
    sound_id = Column(Integer, primary_key=True, autoincrement=True)
    question_id = Column(Integer, ForeignKey('Questions.question_id', onupdate='Cascade'), nullable=False)
    sound_url = Column(String(255), nullable=False)

    question = relationship("Questions", back_populates="sounds")

class Images(Base):
    __tablename__ = 'Images'
    image_id = Column(Integer, primary_key=True, autoincrement=True)
    answer_id = Column(Integer, ForeignKey('Answers.answer_id', onupdate='Cascade'), nullable=False)
    image_url = Column(String(255), nullable=False)

    answer = relationship("Answers", back_populates="images")