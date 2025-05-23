from fastapi import APIRouter, HTTPException, Query
from app.models.generation_history import GenerationHistory

router = APIRouter()
history_model = GenerationHistory()

@router.get("/history")
async def get_history_list(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """Mendapatkan daftar history generasi."""
    try:
        history_list = history_model.get_history_list(limit=limit, offset=offset)
        return {
            "success": True,
            "data": history_list
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching history list: {str(e)}"
        )

@router.get("/history/{history_id}")
async def get_history_detail(history_id: int):
    """Mendapatkan detail history generasi berdasarkan ID."""
    try:
        history = history_model.get_history_by_id(history_id)
        if not history:
            raise HTTPException(
                status_code=404,
                detail=f"History with ID {history_id} not found"
            )
        return {
            "success": True,
            "data": history
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching history detail: {str(e)}"
        )

@router.get("/content/{content_id}/history")
async def get_content_history(
    content_id: int,
    limit: int = Query(10, ge=1, le=50)
):
    """Mendapatkan daftar history generasi untuk konten tertentu."""
    try:
        history_list = history_model.get_history_by_content_id(
            content_id=content_id,
            limit=limit
        )
        return {
            "success": True,
            "data": history_list
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching content history: {str(e)}"
        )

@router.get("/history/search")
async def search_history(
    q: str = Query("", min_length=1),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """Mencari history generasi berdasarkan judul topik."""
    try:
        if not q:
            return {
                "success": True,
                "data": []
            }
            
        history_list = history_model.search_history(
            search_term=q,
            limit=limit,
            offset=offset
        )
        return {
            "success": True,
            "data": history_list
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error searching history: {str(e)}"
        )