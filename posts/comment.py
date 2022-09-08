from datetime import datetime
from fastapi import APIRouter, Depends, status, HTTPException
from posts.posts_schemas import (
    CreateCommentForm,
    CommentView,
    UserView,
    EditCommentForm,
)
from user.auth import get_current_user, get_user_exception
from database.models import Comments
from database.session import get_db
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import joinedload
from sqlalchemy import exc


router = APIRouter(
    prefix="/comment",
    tags=["comments"],
    responses={404: {"description": "Not found"}},
)

# Route to get specific comment by ID (Login required):


@router.get("/{id}")
async def get_comment_by_id(
    id: int,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    if user is None:
        raise get_user_exception()
    else:
        result = db.query(Comments).filter(Comments.id == id).first()

        return CommentView(
            comment_id=result.id,
            content=result.content,
            comment_date=result.comment_date,
            author=UserView(
                user_id=result.author.id,
                full_name=f"{result.author.first_name} {result.author.last_name}".title(),
                avatar=result.author.avatar,
            ),
        )


# Route to get (logged) users comments (Login required):


@router.get("/user/{id}")
async def get_all_users_comments(
    user: dict = Depends(get_current_user), db: Session = Depends(get_db)
):

    if user is None:
        raise get_user_exception()

    return [
        CommentView(
            comment_id=result.id,
            content=result.content,
            comment_date=result.comment_date,
            author=UserView(
                user_id=result.author.id,
                full_name=f"{result.author.first_name} {result.author.last_name}".title(),
                avatar=result.author.avatar,
            ),
        )
        for result in db.query(Comments)
        .filter(Comments.author_id == user.get("id"))
        .options(joinedload("author"))
        .all()
    ]


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

    try:
        db.add(comment_model)
        db.commit()
        return successful_response(201)
    except exc.SQLAlchemyError as e:
        db.rollback()
        return unsuccessful_response(400)


# Route to edit comment (Login required):


@router.put("/{id}")
async def edit_comment(
    id: int,
    comment: EditCommentForm,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    if user is None:
        raise get_user_exception()

    comment_model = (
        db.query(Comments)
        .filter(Comments.id == id)
        .filter(Comments.author_id == user.get("id"))
        .first()
    )
    comment_model.content = comment.content

    if comment.content:
        try:
            db.add(comment_model)
            db.commit()
            return successful_response(201)

        except exc.SQLAlchemyError as e:
            db.rollback()
            return unsuccessful_response(400)
    else:
        return unsuccessful_response(400)


# Route to delete comment (Login required):


@router.delete("/{id}")
async def delete_comment(
    id: int,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    if user is None:
        raise get_user_exception()

    post_model = (
        db.query(Comments)
        .filter(Comments.id == id)
        .filter(Comments.author_id == user.get("id"))
        .first()
    )
    if post_model is None:
        raise http_exception()

    try:
        db.query(Comments).filter(Comments.id == id).delete()
        db.commit()
        return successful_response(200)

    except exc.SQLAlchemyError as e:
        db.rollback()
        return unsuccessful_response(400)


def http_exception():
    return HTTPException(status_code=404, detail="Post not found!")


def successful_response(status_code: int):
    return {"status": 200, "transaction": "Successful"}


def unsuccessful_response(status_code: int):
    return {"status": 400, "transaction": "Unsuccessful"}
