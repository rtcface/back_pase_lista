from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker 
from sqlalchemy.ext.declarative import declarative_base
from decouple import config
from config.settings import *

#nurl = "postgresql+psycopg://postgres:postgres@localhost:5432/postgres"

url = URL.create(settings.POSTGRES_DB_DRIVER, config("POSTGRES_USER"), config("POSTGRES_PASSWORD"), config("POSTGRES_HOST"), config("POSTGRES_PORT"), config("POSTGRES_DB"))
engine = create_engine(url, connect_args={"connect_timeout": 5})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




