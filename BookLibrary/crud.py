from sqlalchemy import UUID
from sqlalchemy.orm import Session
import models, schemas, utils
from fastapi import HTTPException

# Author CRUD
def get_author(db: Session, author_id: UUID):
    return db.query(models.Author).filter(models.Author.id == author_id).first()

def get_authors(db: Session, skip: int = 0, limit: int = 10):
    # return db.query(models.Author).offset(skip).limit(limit).all()
    return db.query(models.Author)[skip:skip + limit]

def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.Author(**author.dict())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

def update_author(db: Session, author_id: UUID, author: schemas.AuthorCreate):
    db_author = get_author(db, author_id)
    if not db_author:
        return None
    for key, value in author.dict().items():
        setattr(db_author, key, value)
    db.commit()
    db.refresh(db_author)
    return db_author

def delete_author(db: Session, author_id: UUID):
    db_author = get_author(db, author_id)
    if db_author:
        db.delete(db_author)
        db.commit()
        return db_author
    return None

# Category CRUD
def get_category(db: Session, category_id: UUID): # category by id
    return db.query(models.Category).filter(models.Category.id == category_id).first()

def get_all_categories(db: Session, skip: int = 0): # list of all categories
    return db.query(models.Category).offset(skip).all()

def create_category(db: Session, category: schemas.CategoryCreate):
    db_category = models.Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def update_category(db: Session, category_id: UUID, category: schemas.CategoryCreate):
    db_category = get_category(db, category_id)
    if not db_category:
        return None
    for key, value in category.dict().items():
        setattr(db_category, key, value)
    db.commit()
    db.refresh(db_category)
    return db_category

def delete_category(db: Session, category_id: UUID):
    db_category = get_category(db, category_id)
    if db_category:
        db.delete(db_category)
        db.commit()
        return db_category
    return None


# Book CRUD
def get_book(db: Session, book_id: UUID): # book by id
    return db.query(models.Book).filter(models.Book.id == book_id).first()

def get_all_books(db: Session, skip: int = 0): # list of all categories
    return db.query(models.Book).offset(skip).all()

def create_book(db: Session, book: schemas.BookCreate):
    category_ids = book.category_ids

    book_data = book.dict()
    book_data.pop('category_ids')

    db_book = models.Book(**book_data)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)

    for category_id in category_ids:
        category = db.query(models.Category).filter(models.Category.id == category_id).first()
        if category:
            db_book.categories.append(category)

    db.commit()
    db.refresh(db_book)
    return db_book

# def update_book(db: Session, book_id: UUID, book: schemas.BookCreate):
#     db_book = get_book(db, book_id)
#     if not db_book:
#         return None
#     for key, value in book.dict().items():
#         setattr(db_book, key, value)
#     db.commit()
#     db.refresh(db_book)
#     return db_book
def update_book(db: Session, book_id: UUID, book: schemas.BookCreate):
    db_book = get_book(db, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    # Check if the new author exists
    author = db.query(models.Author).filter(models.Author.id == book.author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    # Update book details
    book_data = book.dict()
    category_ids = book_data.pop('category_ids')

    for key, value in book_data.items():
        setattr(db_book, key, value)

    # Clear current categories
    db_book.categories.clear()

    # Add new categories
    for category_id in category_ids:
        category = db.query(models.Category).filter(models.Category.id == category_id).first()
        if category:
            db_book.categories.append(category)

    db.commit()
    db.refresh(db_book)
    return db_book

def delete_book(db: Session, book_id: UUID):
    db_book = get_book(db, book_id)
    if db_book:
        db.delete(db_book)
        db.commit()
        return True
    return None



# user Authentication
def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = utils.get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


