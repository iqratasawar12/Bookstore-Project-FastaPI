import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, ForeignKey, Table, Date, Enum, UUID, Boolean
from sqlalchemy.orm import relationship
import uuid

Base = declarative_base()


# Association table for many-to-many relationship between books and categories
book_category = Table(
    'book_category', Base.metadata,
    Column('book_id', UUID(as_uuid=True), ForeignKey('books.id')),
    Column('category_id', UUID(as_uuid=True), ForeignKey('categories.id'))
)


class Author(Base):
    __tablename__ = "authors"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    DOB = Column(Date)
    gender = Column(Enum("male", "female", "other", name="gender_enum"))
    country = Column(String)
    email = Column(String, unique=True, index=True)

    books = relationship("Book", back_populates="author")
    # books = relationship("Book", back_populates="authors")



class Category(Base):
    __tablename__ = "categories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category_name = Column(String, unique=True, index=True)

    books = relationship("Book", secondary=book_category, back_populates="categories")



class Book(Base):
    __tablename__ = "books"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, index=True)
    description = Column(String)
    author_id = Column(UUID(as_uuid=True), ForeignKey('authors.id'))

    author = relationship("Author", back_populates="books")
    categories = relationship("Category", secondary=book_category, back_populates="books")


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    disabled = Column(Boolean, default=False)

