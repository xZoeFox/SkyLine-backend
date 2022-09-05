from datetime import datetime
from fastapi import APIRouter, Depends
from posts.posts_schemas import CreateCommentForm
from user.auth import get_current_user, get_user_exception
from database.models import Comments
from database.session import get_db
from sqlalchemy.orm.session import Session


router = APIRouter(
    prefix="/comment",
    tags=["comments"],
    responses={404: {"description": "Not found"}},
)

# Route to get all comments (Login not required):


@router.get("/")
async def read_all(
    db: Session = Depends(get_db),
):
    return db.query(Comments).all()


# Route to get specific (logged) users comments (Login required):


@router.get("/user")
async def read_all_by_user(
    user: dict = Depends(get_current_user), db: Session = Depends(get_db)
):

    if user is None:
        raise get_user_exception()

    return db.query(Comments).filter(Comments.author_id == user.get("id")).all()


# Route to create comment (Login required):


@router.post("/")
async def create_comment(
    comment: CreateCommentForm,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    if user is None:
        raise get_user_exception()

    comment_model = Comments()
    comment_model.content = comment.content
    comment_model.comment_date = datetime.now()
    comment_model.author_id = user.get("id")
    comment_model.post_id = comment.post_id

    db.add(comment_model)
    db.commit()

    return successful_response(201)


def successful_response(status_code: int):
    return {"status": 200, "transaction": "Successful"}
