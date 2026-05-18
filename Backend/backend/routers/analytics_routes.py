from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Prompt
from utils.auth_dependency import get_current_user

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/analytics/user")
def get_user_analytics(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    prompts = db.query(Prompt).filter(Prompt.user_id == user.id).all()

    total_prompts = len(prompts)

    if total_prompts == 0:
        return {
            "total_prompts": 0,
            "average_score": 0,
            "difficulty_distribution": {}
        }

    # ✅ FIXED SCORE CALCULATION
    valid_scores = [p.overall_score for p in prompts if p.overall_score is not None]

    if len(valid_scores) == 0:
        avg_score = 0
    else:
        avg_score = sum(valid_scores) / len(valid_scores)

    difficulty_count = {}
    for p in prompts:
        difficulty_count[p.difficulty] = difficulty_count.get(p.difficulty, 0) + 1

    return {
        "total_prompts": total_prompts,
        "average_score": round(avg_score, 2),
        "difficulty_distribution": difficulty_count
    }