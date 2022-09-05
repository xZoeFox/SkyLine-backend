from datetime import datetime
from fastapi import APIRouter, Depends
from posts.posts_schemas import CreatePostForm, PostView, UserView, CommentView
from user.auth import get_current_user, get_user_exception
from database.models import Posts
from database.session import get_db
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import joinedload


router = APIRouter(
    prefix="/post",
    tags=["posts"],
    responses={404: {"description": "Not found"}},
)

# Route to get all posts (Login not required):
"""It will show all post info, with owner fullname and id & comments with their authors info"""


@router.get("/")
async def read_all(
    db: Session = Depends(get_db),
):
    return [
        PostView(
            post_id=result.id,
            content=result.content,
            post_date=result.post_date,
            like_count=result.like_count,
            owner=UserView(
                user_id=result.owner.id,
                full_name=f"{result.owner.first_name} {result.owner.last_name}".title(),
            ),
            comments=[
                CommentView(
                    comment_id=comment.id,
                    content=comment.content,
                    comment_date=comment.comment_date,
                    author=UserView(
                        user_id=comment.author.id,
                        full_name=f"{comment.author.first_name} {comment.author.last_name}".title(),
                    ),
                )
                for comment in result.comments
            ],
        )
        for result in db.query(Posts)
        .options(joinedload("owner"))
        .options(joinedload("comments"))
        .all()
    ]


# Route to get specific (logged) users posts (Login required):


@router.get("/user")
async def read_all_by_user(
    user: dict = Depends(get_current_user), db: Session = Depends(get_db)
):

    if user is None:
        raise get_user_exception()

    return db.query(Posts).filter(Posts.owner_id == user.get("id")).all()


# Route to create post (Login required):


@router.post("/")
async def create_post(
    post: CreatePostForm,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    if user is None:
        raise get_user_exception()

    post_model = Posts()
    post_model.content = post.content
    post_model.post_date = datetime.now()
    post_model.owner_id = user.get("id")

    db.add(post_model)
    db.commit()

    return successful_response(201)


def successful_response(status_code: int):
    return {"status": 200, "transaction": "Successful"}
