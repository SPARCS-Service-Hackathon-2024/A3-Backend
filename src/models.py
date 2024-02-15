from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime, Text, text
from sqlalchemy.dialects.mysql import BIGINT, DATETIME, DATE, INTEGER
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class LUsers(Base):
    __tablename__ = 'Users'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=True)
    birthday = Column(DateTime, nullable=True)
    call = Column(String(255), nullable=True)
    address = Column(String(255), nullable=True)
    created_at = Column(DATETIME(fsp=3), nullable=False, server_default=text("CURRENT_TIMESTAMP(3)"))


# class LQuestions(Base):
#     __tablename__ = 'Questions'
#     question_id = Column(Integer, primary_key=True, autoincrement=True)
#     is_fixed = Column(Boolean, nullable=False, default=False)
#     user_id = Column(Integer, ForeignKey('LUsers.user_id', onupdate='Cascade'), nullable=False)
#     parents_id = Column(Integer, nullable=False)
#     content = Column(Text, nullable=False)
#     created_at = Column(DATETIME(fsp=3), nullable=False, server_default=text("CURRENT_TIMESTAMP(3)"))

#     user = relationship("LUsers", back_populates="questions")
#     answers = relationship("LAnswers", back_populates="question")
#     sounds = relationship("LSound", back_populates="question")

# class LAnswers(Base):
#     __tablename__ = 'Answers'
#     answer_id = Column(Integer, primary_key=True, autoincrement=True)
#     question_id = Column(Integer, ForeignKey('LQuestions.question_id', onupdate='Cascade'), nullable=False)
#     user_id = Column(Integer, ForeignKey('LUsers.user_id', onupdate='Cascade'), nullable=False)
#     content = Column(Text, nullable=False)
#     created_at = Column(DATETIME(fsp=3), nullable=False, server_default=text("CURRENT_TIMESTAMP(3)"))

#     question = relationship("LQuestions", back_populates="answers")
#     user = relationship("LUsers", back_populates="answers")
#     images = relationship("LImages", back_populates="answer")

# class LSound(Base):
#     __tablename__ = 'Sound'
#     sound_id = Column(Integer, primary_key=True, autoincrement=True)
#     question_id = Column(Integer, ForeignKey('LQuestions.question_id', onupdate='Cascade'), nullable=False)
#     sound_url = Column(String(255), nullable=False)

#     question = relationship("LQuestions", back_populates="sounds")

# class LImages(Base):
#     __tablename__ = 'Images'
#     image_id = Column(Integer, primary_key=True, autoincrement=True)
#     answer_id = Column(Integer, ForeignKey('LAnswers.answer_id', onupdate='Cascade'), nullable=False)
#     image_url = Column(String(255), nullable=False)

#     answer = relationship("LAnswers", back_populates="images")