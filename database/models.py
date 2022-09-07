from sqlalchemy import (
    ForeignKey,
    Boolean,
    Column,
    Integer,
    String,
    Date,
    DateTime,
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata

# Models:


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(30), nullable=False)
    last_name = Column(String(30), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    date_joined = Column(Date, nullable=False)
    birth_date = Column(Date, nullable=True)
    avatar = Column(String(200), nullable=True)
    description = Column(String(500), nullable=True)
    active = Column(Boolean, default=True)

    posts = relationship("Posts", back_populates="owner")
    comments = relationship("Comments", back_populates="author")

class Comments(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True)
    content = Column(String(250), nullable=False)
    comment_date = Column(DateTime, nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"))
    author_id = Column(Integer, ForeignKey("users.id"))

    author = relationship("Users", back_populates="comments" , cascade="all, delete-orphan")
    posts = relationship("Posts", back_populates="comments", cascade="all, delete-orphan")

class Posts(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    content = Column(String(500), nullable=False)
    post_date = Column(DateTime, nullable=False)
    like_count = Column(Integer, default=0)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("Users", back_populates="posts", cascade="all, delete-orphan")
    comments = relationship("Comments", back_populates="posts")


