from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# CreateSchemas:


class CreatePostForm(BaseModel):
    content: str

    class Config:
        orm_mode = True


class EditPostForm(BaseModel):
    content: Optional[str]

    class Config:
        orm_mode = True


class CreateCommentForm(BaseModel):
    content: str
    post_id: int

    class Config:
        orm_mode = True


class EditCommentForm(BaseModel):
    content: Optional[str]

    class Config:
        orm_mode = True


# ViewSchemas:


class UserView(BaseModel):
    user_id: int
    full_name: str
    avatar: Optional[str]

    class Config:
        orm_mode = True


class CommentView(BaseModel):
    comment_id: int
    content: str
    comment_date: datetime
    author: UserView

    class Config:
        orm_mode = True


class PostView(BaseModel):
    post_id: int
    content: str
    post_date: datetime
    like_count: int
    owner: UserView
    comments: List[CommentView]

    class Config:
        orm_mode = True
