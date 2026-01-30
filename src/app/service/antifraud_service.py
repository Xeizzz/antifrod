#логика сервиса
from datetime import datetime, date
from app.models.model_antifraud import AntifraudRequest, AntifraudResponse
import json
from app.redis_client import get, set

class AntifraudService:

    @staticmethod
    def calculate_age(birth_date_str: str) -> int:
        birth_date = datetime.strptime(birth_date_str, "%d.%m.%Y").date()
        today = date.today()

        age = today.year - birth_date.year
        if (today.month, today.day) < (birth_date.month, birth_date.day):
            age -= 1

        return age

    @staticmethod
    def is_adult(birth_date_str: str) -> bool:
        return AntifraudService.calculate_age(birth_date_str) >= 18

    @classmethod
    async def check_client(cls, request: AntifraudRequest) -> AntifraudResponse:

        cache_key = f"antifraud:{request.phone_number}"

        cached_result = await get(cache_key)
        if cached_result:
            return AntifraudResponse(**json.loads(cached_result))

        stop_factors = []

        if not cls.is_adult(request.birth_date):
            age = cls.calculate_age(request.birth_date)
            stop_factors.append(f"Клиент младше 18 лет (возраст: {age})")

        unclosed_loans = [loan for loan in request.loans_history if not loan.is_closed]
        if unclosed_loans:
            stop_factors.append(f"Найдено {len(unclosed_loans)} незакрытых займов")

        result = AntifraudResponse(
            stop_factors=stop_factors,
            result=len(stop_factors) == 0
        )

        if result.result:
            await set(
                        cache_key,
                        json.dumps(result.model_dump(), ensure_ascii=False)
                    )

        return result