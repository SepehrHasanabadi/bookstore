from typing import Annotated
import os
from datetime import datetime, timedelta
from fastapi import Depends, FastAPI, HTTPException, Request, Response, status
from sqlalchemy.orm import Session
from jose import jwt
from fastapi.middleware.cors import CORSMiddleware
from app import crud, schemas
from app.database import SessionLocal
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


app = FastAPI()
origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_db(request: Request):
    return request.state.db

@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user(db, username: str):
    user = crud.get_user(db, username)
    return user

def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.getenv('SECRET_KEY', ''), algorithm=os.getenv('ALGORITHM', 'HS256'))
    return encoded_jwt

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', 30))
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/authors/", response_model=schemas.Paginated[schemas.AuthorGet])
def get_authors(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db), skip: int | None = None, limit: int | None = None, q: str | None = None):
    db_data = crud.get_authors(db, q=q, skip=skip, limit=limit)
    if db_data.total == 0:
        raise HTTPException(status_code=400, detail="there is no authors")
    return db_data

@app.post("/authors/", response_model=schemas.AuthorGet)
def create_author(token: Annotated[str, Depends(oauth2_scheme)], author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    db_data = crud.create_author(db, author)
    return db_data

@app.put("/authors/{author_id}", response_model={})
def update_author(author_id: int, token: Annotated[str, Depends(oauth2_scheme)], author: schemas.AuthorUpdate, db: Session = Depends(get_db)):
    if (crud.update_author(db, author, author_id) >= 1):
        return {}
    raise HTTPException(status_code=400, detail="author id not found")


@app.post("/bulk_books/")
def save_books(token: Annotated[str, Depends(oauth2_scheme)], data: schemas.BooksCreate, db: Session = Depends(get_db)):
    crud.save_books(db, data.books, data.author_id)
    return {}

@app.post("/books/")
def save_books(token: Annotated[str, Depends(oauth2_scheme)], data: schemas.BookCreate, db: Session = Depends(get_db)):
    db_data = crud.create_book(db, data)
    return db_data

@app.put("/books/{book_id}")
def update_book(book_id: int, token: Annotated[str, Depends(oauth2_scheme)], data: schemas.BookUpdate, db: Session = Depends(get_db)):
    if(crud.update_book(db, data, book_id) >= 1):
        return {}
    raise HTTPException(status_code=400, detail="book id not found")

@app.get("/books/", response_model=schemas.Paginated[schemas.BookGet])
def get_books(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db), skip: int | None = None, limit: int | None = None, q: str | None = None):
    db_data = crud.get_books(db, q=q, skip=skip, limit=limit)
    if db_data.total == 0:
        raise HTTPException(status_code=400, detail="there is no books")
    return db_data

@app.get("/")
def read_root():
    return {"Hello": "World"}
