from sqlalchemy import create_engine, UUID
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, Session

import os
from dotenv import load_dotenv
load_dotenv()


DATABASE_URL = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
print(f'\nDATABASE_URL: {DATABASE_URL}')


# engine = create_engine(DATABASE_URL)
# Session = sessionmaker(bind=engine)
# Base = declarative_base()
# Base.metadata.create_all(bind=engine)
# Session.configure(bind=engine)
# session = Session()

# engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
# print(f'\nengine: {engine}')
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    print(f'\nsession: {db}')
    try:
        yield db
    finally:
        db.close()


