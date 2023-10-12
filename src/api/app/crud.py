from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, username):
    return db.query(models.User).filter(models.User.username == username).first()


def get_author(db: Session, author_id: int):
    return db.query(models.Author).filter(models.Author.id == author_id).first()


def get_authors(db: Session, q: str | None = None, skip: int = 0, limit: int = 100):
    total = db.query(models.Author).count()
    if (q):
        search = "%{}%".format(q.lower())
        items = db.query(models.Author).filter(models.Author.name.ilike(search)).offset(skip).limit(limit).all()
    else:
        items = db.query(models.Author).offset(skip).limit(limit).all()
    return schemas.Paginated(total=total, items=items)



def create_author(db: Session, author: schemas.AuthorCreate):
    db_data = models.Author(**author.dict())
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data


def update_author(db: Session, author: schemas.AuthorUpdate, author_id: int):
    update_count = db.query(models.Author).filter(models.Author.id == author_id).update(author.dict())
    db.commit()
    return update_count
    

def get_books(db: Session, q: str | None = None, skip: int = 0, limit: int = 100):
    total = db.query(models.Book).count()
    if (q):
        search = "%{}%".format(q.lower())
        items = db.query(models.Book).filter(models.Book.name.ilike(search)).offset(skip).limit(limit).all()
    else:
        items = db.query(models.Book).offset(skip).limit(limit).all()
    return schemas.Paginated(total=total, items=items)

def update_book(db: Session, book: schemas.BookUpdate, book_id: int):
    update_count = db.query(models.Book).filter(models.Book.id == book_id).update(book.dict())
    db.commit()
    return update_count

def create_book(db: Session, author: schemas.BookCreate):
    db_data = models.Book(**author.dict())
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data

def save_books(db: Session, books: schemas.BaseBook, author_id: int):
    db.query(models.Book).filter(models.Book.author_id == author_id).delete()
    db_items = [models.Book(**book.dict(), author_id=author_id) for book in books]
    db.bulk_save_objects(db_items)
    db.commit()
