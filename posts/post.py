from datetime import datetime
from fastapi import APIRouter, Depends
from posts.posts_schemas import CreatePostForm
from user.auth import get_current_user, get_user_exception
from database.models import Posts
from database.session import get_db
from sqlalchemy.orm.session import Session


router = APIRouter(
    prefix="/post",
    tags=["posts"],
    responses={404: {"description": "Not found"}},
)

# Route to get all posts (Login not required):


@router.get("/")
async def read_all(
    db: Session = Depends(get_db),
):
    return db.query(Posts).all()


# Route to logged in users posts (Login required):


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
