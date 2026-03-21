from fastapi import APIRouter
from schemas import PromptRequest
from services.nlp_analyzer import analyze_prompt
from services.prompt_classifier import classify_prompt
from services.ai_service import generate_ai_response
from services.feedback_engine import improve_prompt

router = APIRouter()

@router.get("/test")
def test():
    return {"message": "Prompt routes working"}

@router.post("/prompt/full-process")
def full_prompt_process(data: PromptRequest):
    prompt = data.prompt

    analysis = analyze_prompt(prompt)
    level = classify_prompt(prompt)
    improved_prompt = improve_prompt(prompt)
    ai_response = generate_ai_response(improved_prompt)

    return {
        "original_prompt": prompt,
        "analysis": analysis,
        "difficulty_level": level,
        "improved_prompt": improved_prompt,
        "ai_response": ai_response
    }