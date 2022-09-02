from datetime import datetime, timedelta
from email.policy import default
from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    DECIMAL,
    Enum,
    Date,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum
from datetime import date

Base = declarative_base()
metadata = Base.metadata

# Enumerations:


class DealStatus(enum.Enum):
    hot = "hot"
    mild = "mild"
    cold = "cold"




# Models:


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key = True)
    first_name = Column(String(30), nullable = False)
    last_name = Column(String(30), nullable = False)
    email = Column(String(100), unique=True, nullable = False)
    password = Column(String(200), nullable = False)
    date_joined = Column(Date, nullable = False)
    birth_date = Column(Date, nullable = True)
    avatar = Column(String(200), nullable = True)
    description = Column(String(500), nullable = True)
    active = Column(Boolean, default = True)



