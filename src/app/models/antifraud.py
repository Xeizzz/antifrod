#модель
from datetime import datetime
from pydantic import BaseModel, field_validator
from typing import List
import re
from datetime import date, datetime

class Loan(BaseModel):
    amount: float
    loan_date: str
    is_closed: bool = True

    @field_validator('loan_date')
    @classmethod
    def validate_loan_date(cls, v):
        try:
            datetime.strptime(v, "%d.%m.%Y")
            return v
        except ValueError:
            raise ValueError('Дата должна быть в формате DD.MM.YYYY')

class Phone(BaseModel):
    pnumber: str

    @field_validator('pnumber')
    @classmethod
    def validate_pnumber(cls,v):
        if v.startswith('+7'):
            if len(v) != 12:
                raise ValueError('Номер с +7 должен содержать 12 символов')
            if not v[1:].isdigit():
                raise ValueError('Номер должен содержать только цифры и знак +')
        elif v.startswith('8'):
            if len(v) != 11:
                raise ValueError('Номер с 8 должен содержать 11 символов')
            if not v.isdigit():
                raise ValueError('Номер должен содержать только цифры')
        else:
            raise ValueError('Телефон должен начинаться с +7 или 8')
        return v


class BirthDate(BaseModel):
    birthdate: str

    @field_validator('birthdate')
    @classmethod
    def validate_birthdate(cls, v):
        try:
            datetime.strptime(v, "%d.%m.%Y")
            return v
        except ValueError:
            raise ValueError('Дата рождения должна быть в формате DD.MM.YYYY')

    def get_age(self):
        birth_date = datetime.strptime(self.birthdate, "%d.%m.%Y").date()
        today = date.today()
        age = today.year - birth_date.year

        if (today.month, today.day) < (birth_date.month, birth_date.day):
            age -= 1

        return age

    def is_adult(self) -> bool:
        return self.get_age() >= 18


class AntifraudRequest(BaseModel):
    birth_date: str
    phone_number: str
    loans_history: List[Loan] = []

    @field_validator('birth_date', 'phone_number')
    @classmethod
    def validate_fields(cls, v, info):
        if info.field_name == 'birth_date':
            BirthDate(birthdate=v)
        elif info.field_name == 'phone_number':
            Phone(pnumber=v)
        return v
