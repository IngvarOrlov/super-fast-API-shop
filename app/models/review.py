from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship

from app.models.base import Base


class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True, index=True)
    comment = Column(String, nullable=True)
    creation_date = Column(DateTime, default=datetime.now)
    grade = Column(Integer, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)

    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    product = relationship("Product", back_populates="reviews")
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship("User", back_populates="reviews")