from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from starlette import status

from app.backend.db_depends import get_db
from app.models import Review, Product, User
from app.routers.auth import get_customer_user, get_admin_user
from app.schemas import CreateReview

router = APIRouter(prefix="/review", tags=["review"])


@router.get("/")
async def all_reviews(session: Annotated[AsyncSession, Depends(get_db)]):
    query = select(Review).where(Review.is_active == True).order_by(Review.creation_date)
    reviews = await session.scalars(query)
    reviews = reviews.all()
    if not reviews:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No reviews found")
    return reviews


@router.get("/{product_id}")
async def product_reviews(
        session: Annotated[AsyncSession, Depends(get_db)],
        product_id: int
):
    query = select(Product).where(Product.id == product_id)
    product = await session.scalar(query)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")

    query = select(Review).where(
        Review.is_active == True,
        Review.product_id == product_id
    ).order_by(Review.creation_date)
    reviews = await session.scalars(query)
    reviews = reviews.all()
    return reviews


@router.post("/")
async def add_review(
        session: Annotated[AsyncSession, Depends(get_db)],
        review: CreateReview,
        user: Annotated[User, Depends(get_customer_user)],
):
    query = select(Product).options(joinedload(Product.reviews)).where(Product.is_active == True)
    product = await session.scalar(query)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    reviews = [review for review in product.reviews if review.is_active == True]
    grade_sum = sum([review.grade for review in reviews]) + review.grade
    grade = round(grade_sum / (len(reviews) + 1), 1)

    query = insert(Review).values(
        comment=review.comment,
        grade=review.grade,
        product_id=review.product_id,
        user_id=user.get('id')
    )
    await session.execute(query)
    await session.execute(update(Product).where(Product.id == product.id).values(rating=grade))
    await session.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}


@router.delete("/{product_id}")
async def delete_review(
        session: Annotated[AsyncSession, Depends(get_db)],
        review_id: int,
        _: Annotated[User, Depends(get_admin_user)]
):
    query = select(Review).where(Review.id == review_id, Review.is_active == True)
    review = await session.scalar(query)
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
    delete_query = update(Review).where(Review.id == review_id).values(is_active=False)

    reviews_query = select(Review).where(
        Review.is_active == True,
        Review.product_id == review.product_id,
        Review.id != review.id)
    reviews = await session.scalars(reviews_query)
    reviews = reviews.all()
    rating = round(sum([review.grade for review in reviews]) / len(reviews), 1)
    update_rating_query = update(Product).where(Product.id == review.product_id).values(rating=rating)

    await session.execute(delete_query)
    await session.execute(update_rating_query)
    await session.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'Successful'}
