from typing import Optional
from pydantic import BaseModel


class RegisterForm(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    password_repeat: str

    class Config:
        orm_mode = True


class EditProfileForm(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    birth_date: Optional[str]
    avatar: Optional[str]
    description: Optional[str]

    class Config:
        orm_mode = True
