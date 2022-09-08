from datetime import datetime
from fastapi import APIRouter, Depends, status, HTTPException
from posts.posts_schemas import (
    CreatePostForm,
    EditPostForm,
    PostView,
    UserView,
    CommentView,
)
from user.auth import get_current_user, get_user_exception
from database.models import Posts
from database.session import get_db
from sqlalchemy.orm.session import Session
from sqlalchemy.orm import joinedload
from sqlalchemy import exc


router = APIRouter(
    prefix="/post",
    tags=["posts"],
    responses={404: {"description": "Not found"}},
)

# Route to get all posts (Login not required):
"""It will show all post info, with owner fullname and id & comments with their authors info"""


@router.get("/")
async def get_all_posts(
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
                avatar=result.owner.avatar,
            ),
            comments=[
                CommentView(
                    comment_id=comment.id,
                    content=comment.content,
                    comment_date=comment.comment_date,
                    author=UserView(
                        user_id=comment.author.id,
                        full_name=f"{comment.author.first_name} {comment.author.last_name}".title(),
                        avatar=comment.author.avatar,
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


# Route to get specific post by ID (Login required):


@router.get("/{id}")
async def get_post_by_id(
    id: int,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    if user is None:
        raise get_user_exception()
    else:
        result = (
            db.query(Posts)
            .options(joinedload("owner"))
            .options(joinedload("comments"))
            .get(id)
        )

        return PostView(
            post_id=result.id,
            content=result.content,
            post_date=result.post_date,
            like_count=result.like_count,
            owner=UserView(
                user_id=result.owner.id,
                full_name=f"{result.owner.first_name} {result.owner.last_name}".title(),
                avatar=result.owner.avatar,
            ),
            comments=[
                CommentView(
                    comment_id=comment.id,
                    content=comment.content,
                    comment_date=comment.comment_date,
                    author=UserView(
                        user_id=comment.author.id,
                        full_name=f"{comment.author.first_name} {comment.author.last_name}".title(),
                        avatar=comment.author.avatar,
                    ),
                )
                for comment in result.comments
            ],
        )


# Route to get (logged) users posts (Login required):


@router.get("/user/{id}")
async def get_all_users_posts(
    user: dict = Depends(get_current_user), db: Session = Depends(get_db)
):

    if user is None:
        raise get_user_exception()

    return [
        PostView(
            post_id=result.id,
            content=result.content,
            post_date=result.post_date,
            like_count=result.like_count,
            owner=UserView(
                user_id=result.owner.id,
                full_name=f"{result.owner.first_name} {result.owner.last_name}".title(),
                avatar=result.owner.avatar,
            ),
            comments=[
                CommentView(
                    comment_id=comment.id,
                    content=comment.content,
                    comment_date=comment.comment_date,
                    author=UserView(
                        user_id=comment.author.id,
                        full_name=f"{comment.author.first_name} {comment.author.last_name}".title(),
                        avatar=comment.author.avatar,
                    ),
                )
                for comment in result.comments
            ],
        )
        for result in db.query(Posts)
        .filter(Posts.owner_id == user.get("id"))
        .options(joinedload("owner"))
        .options(joinedload("comments"))
        .all()
    ]


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

    try:
        db.add(post_model)
        db.commit()
        return successful_response(201)
    except exc.SQLAlchemyError as e:
        db.rollback()
        return unsuccessful_response(400)


# Route to edit post (Login required):


@router.put("/{id}")
async def edit_post(
    id: int,
    post: EditPostForm,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    if user is None:
        raise get_user_exception()

    post_model = (
        db.query(Posts)
        .filter(Posts.id == id)
        .filter(Posts.owner_id == user.get("id"))
        .first()
    )
    post_model.content = post.content

    if post.content:
        try:
            db.add(post_model)
            db.commit()
            return successful_response(201)

        except exc.SQLAlchemyError as e:
            db.rollback()
            return unsuccessful_response(400)
    else:
        return unsuccessful_response(400)


# Route to delete post (Login required):


@router.delete("/{id}")
async def delete_post(
    id: int,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):

    if user is None:
        raise get_user_exception()

    post_model = (
        db.query(Posts)
        .filter(Posts.id == id)
        .filter(Posts.owner_id == user.get("id"))
        .first()
    )
    if post_model is None:
        raise http_exception()

    try:
        db.query(Posts).filter(Posts.id == id).delete()
        db.commit()
        return successful_response(200)

    except exc.SQLAlchemyError as e:
        print(e)
        db.rollback()
        return unsuccessful_response(400)


def http_exception():
    return HTTPException(status_code=404, detail="Post not found!")


def successful_response(status_code: int):
    return {"status": 200, "transaction": "Successful"}


def unsuccessful_response(status_code: int):
    return {"status": 400, "transaction": "Unsuccessful"}
