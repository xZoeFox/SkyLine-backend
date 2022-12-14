from datetime import date
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
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    old_password: Optional[str]
    new_password: Optional[str]
    repeat_password: Optional[str]
    birth_date: Optional[date]
    avatar: Optional[str]
    description: Optional[str]

    class Config:
        orm_mode = True


class ShowMyProfileForm(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    birth_date: Optional[date]
    avatar: Optional[str]
    description: Optional[str]

    class Config:
        orm_mode = True


class ShowProfileForm(BaseModel):
    id: int
    first_name: str
    last_name: str
    birth_date: Optional[date]
    avatar: Optional[str]
    description: Optional[str]

    class Config:
        orm_mode = True
