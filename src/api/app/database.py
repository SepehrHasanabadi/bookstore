from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

SQLALCHEMY_DATABASE_URL = f'postgresql://{os.getenv("POSTGRES_USER", "postgres")}:{os.getenv("POSTGRES_PASSWORD", "password")}@{os.getenv("POSTGRES_HOST", "localhost")}/{os.getenv("POSTGRES_DB", "postgres")}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
