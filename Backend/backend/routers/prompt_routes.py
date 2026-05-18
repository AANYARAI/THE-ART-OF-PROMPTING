from utils.auth_dependency import get_current_user
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from schemas import PromptRequest
from models import Prompt
from services.nlp_analyzer import analyze_prompt
from services.prompt_classifier import classify_prompt
from services.ai_service import generate_ai_response
from services.feedback_engine import improve_prompt

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/test")
def test():
    return {"message": "Prompt routes working"}


@router.post("/prompt/full-process")
def full_prompt_process(
    data: PromptRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    prompt = data.prompt

    analysis = analyze_prompt(prompt)
    level = classify_prompt(prompt)
    improved_prompt = improve_prompt(prompt)
    ai_response = generate_ai_response(improved_prompt)

    # Save to database
    new_prompt = Prompt(
        user_id=user.id,
        prompt_text=prompt,
        improved_prompt=improved_prompt,
        ai_response=ai_response,
        clarity_score=analysis.get("clarity"),
        structure_score=analysis.get("structure"),
        specificity_score=analysis.get("specificity"),
        length_score=analysis.get("length"),
        overall_score=analysis.get("overall_score"),
        difficulty=level
    )

    db.add(new_prompt)
    db.commit()
    db.refresh(new_prompt)

    return {
        "original_prompt": prompt,
        "analysis": analysis,
        "difficulty_level": level,
        "improved_prompt": improved_prompt,
        "ai_response": ai_response
    }

@router.get("/prompt/history")
def get_prompt_history(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    prompts = db.query(Prompt).filter(Prompt.user_id == user.id).all()
    return prompts



@router.get("/prompt/{prompt_id}")
def get_prompt(prompt_id: int, db: Session = Depends(get_db)):
    prompt = db.query(Prompt).filter(
    Prompt.id == prompt_id,
    Prompt.user_id == user.id
).first()

    if not prompt:
        return {"error": "Prompt not found"}

    return prompt


@router.delete("/prompt/{prompt_id}")
def delete_prompt(prompt_id: int, db: Session = Depends(get_db)):
    prompt = db.query(Prompt).filter(
    Prompt.id == prompt_id,
    Prompt.user_id == user.id
).first()

    if not prompt:
        return {"error": "Prompt not found"}

    db.delete(prompt)
    db.commit()

    return {"message": "Prompt deleted"}