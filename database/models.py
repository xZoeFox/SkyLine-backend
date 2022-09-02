from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    Date,
)
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
