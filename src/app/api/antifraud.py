from fastapi import APIRouter, HTTPException
from typing import List


from app.models.antifraud import AntifraudRequest, AntifraudResponse
from app.service.antifraud_service import AntifraudService



router = APIRouter(
    prefix="/antifraudcheck", 
    tags=["antifraud"],
)

@router.post("/check")
async def check_antifraud(request: AntifraudRequest) -> AntifraudResponse:
    """Эндпоинт проверки антифрода"""
    return AntifraudService.check_client(request)