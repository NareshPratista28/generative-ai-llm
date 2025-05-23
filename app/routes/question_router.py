from fastapi import APIRouter, HTTPException
from app.services.llm_service import LLMService

router = APIRouter()
llm_service = LLMService()

@router.get("/generate-question/{content_id}")
async def generate_question(content_id: int):
    try:
        response, generation_time, history_id = llm_service.generate_question(content_id)
        return {
            **response,
            "generation_time": round(generation_time, 2),
            "history_id": history_id
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error generating question: {str(e)}"
        )