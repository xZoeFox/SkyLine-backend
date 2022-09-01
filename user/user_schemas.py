from datetime import date, datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, validator


class RegisterForm(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    date_joined: date
    birth_date: Optional[date]
    avatar: Optional[str]
    description: Optional[str]
    acive: bool

    class Config:
        orm_mode = True