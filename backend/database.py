from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from urllib.parse import quote_plus

USERNAME = "root"
PASSWORD = quote_plus("Revanth@8897")  # encode special chars
HOST = "localhost"
PORT = "3306"
DB_NAME = "ecommerce"

# Correct URL format — note the "//" after mysql+pymysql:
DATABASE_URL = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
