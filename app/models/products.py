from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship
from app.models.base import Base
from app.models.user import User

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    slug = Column(String, unique=True, index=True)
    description = Column(String)
    price = Column(Integer)
    image_url = Column(String)
    stock = Column(Integer)
    rating = Column(Integer)
    is_active = Column(Boolean, default=True)

    reviews = relationship("Review", back_populates="product")
    user_id = Column(Integer, ForeignKey('users.id'))
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship('Category', back_populates='products')




# from sqlalchemy.schema import CreateTable
# print(CreateTable(Product.__table__))