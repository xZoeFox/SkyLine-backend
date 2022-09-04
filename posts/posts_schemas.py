from pydantic import BaseModel


class CreatePostForm(BaseModel):
    content: str

    class Config:
        orm_mode = True
