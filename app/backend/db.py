from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from dotenv import load_dotenv
import os
load_dotenv()

DB_URL = os.getenv("DB_URL")
engine = create_async_engine(DB_URL, echo=True)
# engine = create_engine('sqlite:///my.db', echo=True)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
SessionLocal = sessionmaker(bind=engine)

# from app.models import Base
# Base.metadata.create_all(bind=engine)