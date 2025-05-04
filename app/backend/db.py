import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import sessionmaker

load_dotenv()

DB_URL = os.getenv("DB_URL")
DEBUG = True if os.getenv("DEBUG") == 'True' else False
engine = create_async_engine(DB_URL, echo=DEBUG)
# engine = create_engine('sqlite:///my.db', echo=True)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
SessionLocal = sessionmaker(bind=engine)

# from app.models import Base
# Base.metadata.create_all(bind=engine)