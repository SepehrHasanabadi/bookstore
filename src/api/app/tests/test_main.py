from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from passlib.context import CryptContext
from app import models
from app.database import Base
from main import app, get_db

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_create_user():
    hashed_password = get_password_hash('password')
    db = TestingSessionLocal()
    db_data = models.User(username='bob', hashed_password=hashed_password)
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    token = f'Bearer {hashed_password}'
    headers = {
        'Authorization': token
    }
    empty_authors_response = client.get(
        "/authors/",
        headers= headers
    )
    assert empty_authors_response.status_code == 400
    db_data = models.Author(name='test author')
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    authors_response = client.get(
        "/authors/",
        headers= headers
    )
    assert authors_response.status_code == 200
    data = authors_response.json()
    assert data['items'][0]['name'] == 'test author'
    assert data['total'] == 1
    
