from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# We will use SQLite for local development so no Docker is strictly required initially, 
# but it's easy to swap to PostgreSQL via environment variable.
SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False} # only needed for sqlite
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
