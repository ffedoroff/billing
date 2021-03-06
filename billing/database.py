from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:example@localhost:15432/postgres"
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:example@db:5432/postgres"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
