from pydantic import BaseModel
from typing import Generic, TypeVar, List
from pydantic.generics import GenericModel


class BaseBook(BaseModel):
    name: str
    number_page: int

class Book(BaseBook):
    id: int
    class Config:
        orm_mode = True

class BooksCreate(BaseModel):
    author_id: int
    books: list[BaseBook] = []

class BookUpdate(BaseModel):
    author_id: int
    name: str
    number_page: int

class BookCreate(BaseModel):
    author_id: int
    name: str
    number_page: int

class AuthorBase(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class BookGet(BaseModel):
    id: int
    name: str
    number_page: int
    author: AuthorBase | None = None

    class Config:
        orm_mode = True
    
class AuthorGet(AuthorBase):
    books: list[Book] = []

    class Config:
        orm_mode = True

class AuthorCreate(BaseModel):
    name: str

class AuthorUpdate(BaseModel):
    name: str

class User(BaseModel):
    username: str
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

M = TypeVar('M')

class Paginated(GenericModel, Generic[M]):
    total: int
    items: List[M]