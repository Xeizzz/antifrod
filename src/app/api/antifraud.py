from fastapi import APIRouter, Response, status, Depends


router = APIRouter(
    prefix="/antifraudcheck",
    tags=["antifraud"],
)

@router.post(
"/check",
response_model=
summary="Проверка на стоп-факторы"
response_description="Результат проверки"
)
