from datetime import timedelta
from typing import List
import uvicorn
from fastapi import FastAPI, Depends, HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from uuid import UUID
import models, schemas, crud, db, utils


app = FastAPI()
models.Base.metadata.create_all(bind=db.engine)

# create author
@app.post("/authors", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(db.get_db)):
    return crud.create_author(db=db, author=author)
    # author = crud.create_author(db=db, author=author)
    # if author:
    #     response_ = {
    #         'message': f'Author created successfully',
    #         'status': status.HTTP_201_CREATED,
    #         'data': author
    #     }
    #     return response_
    # raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error in creating author")


@app.get("/authors/{author_id}", response_model=schemas.Author)
def read_author(author_id: UUID, db: Session = Depends(db.get_db)):
    return crud.get_author(db=db, author_id=author_id)
#     author = crud.get_author(db=db, author_id=author_id)
#     if author is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")
#     response_ = {
#         'message': f'Author with id {author_id} found successfully',
#         'status': status.HTTP_200_OK,
#         'id': author_id,
#         'data': author
#     }
#     return response_

# read authors
@app.get("/authors/", response_model=List[schemas.Author])
def read_authors(skip: int = 0, limit: int = 10, db: Session = Depends(db.get_db)):
    authors = crud.get_authors(db, skip=skip, limit=limit)
    return authors


@app.put("/authors/{author_id}", response_model=schemas.Author)
def update_author(author_id: UUID, author: schemas.AuthorCreate, db: Session = Depends(db.get_db)):
    return crud.update_author(db=db, author_id=author_id, author=author)
    # author = crud.update_author(db=db, author_id=author_id, author=author)
    # if author is None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")
    # response_ = {
    #     'message': f'Author with id {author_id} updated successfully',
    #     'status': status.HTTP_200_OK,
    #     'id': author_id,
    #     'data': author
    # }
    # return response_


@app.delete("/authors/{author_id}", response_model=schemas.Author)
def delete_author(author_id: UUID, db: Session = Depends(db.get_db)):
    return crud.delete_author(db=db, author_id=author_id)
    # author = crud.update_author(db=db, author_id=author_id)
    # if author is None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")
    # response_ = {
    #     'message': f'Author with id {author_id} deleted successfully',
    #     'status': status.HTTP_200_OK,
    #     'id': author_id,
    #     'data': author
    # }
    # return response_


# Category endpoints
@app.post("/categories", response_model=schemas.Category)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(db.get_db)):
    return crud.create_category(db=db, category=category)

@app.get("/categories/", response_model=List[schemas.Category])
def read_category(skip: int = 0, db: Session = Depends(db.get_db)):
    return crud.get_all_categories(db, skip=skip)


@app.get("/categories/{category_id}", response_model=schemas.Category)
def read_category(category_id: UUID, db: Session = Depends(db.get_db)):
    return crud.get_category(db=db, category_id=category_id)


@app.put("/categories/{category_id}", response_model=schemas.Category)
def update_category(category_id: UUID, category: schemas.CategoryCreate, db: Session = Depends(db.get_db)):
    return crud.update_category(db=db, category_id=category_id, category=category)


@app.delete("/categories/{category_id}", response_model=schemas.Category)
def delete_category(category_id: UUID, db: Session = Depends(db.get_db)):
    return crud.delete_category(db=db, category_id=category_id)
    # category = crud.delete_category(db=db, category_id=category_id)
    # if category is not None:
    #     response_ = {
    #         "message": "Category deleted successfully",
    #         "status": "success",
    #         "data": category,
    #     }
    #     return response_
    # return {"message": "Category not found", "status": "error"}


# Book endpoints
@app.post("/books", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(db.get_db)):
    return crud.create_book(db=db, book=book)

@app.get("/books/", response_model=List[schemas.Book])
def read_books(skip: int = 0, db: Session = Depends(db.get_db)):
    return crud.get_all_books(db, skip=skip)


@app.get("/books/{book_id}", response_model=schemas.Book)
def read_book(book_id: UUID, db: Session = Depends(db.get_db)):
    return crud.get_book(db=db, book_id=book_id)


@app.put("/books/{book_id}", response_model=schemas.Book)
def update_book(book_id: UUID, book: schemas.BookCreate, db: Session = Depends(db.get_db)):
    return crud.update_book(db=db, book_id=book_id, book=book)


@app.delete("/books/{book_id}", response_model=schemas.Book)
def delete_book(book_id: UUID, db: Session = Depends(db.get_db)):
    book = crud.delete_book(db, book_id)
    return book
    # book = crud.delete_book(db=db, book_id=book_id)
    # if book is True:
    #     return {"message": "Book deleted successfully", "status": "success"}
    # return {"message": "Book not deleted successfully", "status": "error"}


def authenticate_user(db: Session, username: str, password: str):
    user = crud.get_user(db, username=username)
    if not user:
        return False
    if not utils.verify_password(password, user.hashed_password):
        return False
    return user

@app.post("/login", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(db.get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=utils.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = utils.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/users", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(db.get_db)):
    db_user = crud.get_user(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)






if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)




