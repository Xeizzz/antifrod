from fastapi import APIRouter, HTTPException
from typing import List


from app.models.model_antifraud import AntifraudRequest, AntifraudResponse
from app.service.antifraud_service import AntifraudService



router = APIRouter(
    prefix="/antifraud",
    tags=["antifraud"],
)

@router.post("/check")
async def check_antifraud(request: AntifraudRequest) -> AntifraudResponse:
    return await AntifraudService.check_client(request)