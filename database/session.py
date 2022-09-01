from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from database.config import settings


SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)


def get_db():  # for database session
    try:
        print(f"Trying to connect to database: {SQLALCHEMY_DATABASE_URL}")
        db = SessionLocal()
        yield db
    finally:
        db.close()



SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
