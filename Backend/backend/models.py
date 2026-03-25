from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)


class Prompt(Base):
    __tablename__ = "prompts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    prompt_text = Column(Text)
    improved_prompt = Column(Text)
    ai_response = Column(Text)

    clarity_score = Column(Float)
    structure_score = Column(Float)
    specificity_score = Column(Float)
    length_score = Column(Float)
    overall_score = Column(Float)

    difficulty = Column(String)

    created_at = Column(DateTime(timezone=True), server_default=func.now())