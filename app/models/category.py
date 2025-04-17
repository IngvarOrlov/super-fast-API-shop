from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship
from app.models.base import Base

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    slug = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)
    products = relationship("Product", back_populates="category")
    parent_id = Column(Integer, ForeignKey('categories.id'), nullable=True)

    def __repr__(self):
        return '<Category(id={0.id}, name={0.name})>'.format(self)

# from sqlalchemy.schema import CreateTable
# print(CreateTable(Product.__table__))
# print(CreateTable(Category.__table__))
