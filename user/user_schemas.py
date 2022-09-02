from datetime import date, datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, validator


class RegisterForm(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str

    class Config:
        orm_mode = True

class LoginForm(BaseModel):
    email: str
    password: str

    class Config:
        orm_mode = True