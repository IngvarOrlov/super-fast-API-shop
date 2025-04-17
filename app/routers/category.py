from fastapi import APIRouter, Depends, status, HTTPException, Body
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from sqlalchemy import insert, select, update
from slugify import slugify

from app.backend.db_depends import get_db
from app.schemas import CreateCategory
from app.models.category import Category
from app.models.products import Product

router = APIRouter(
    prefix='/categories',
    tags=['category']
)


@router.get('/')
async def get_all_categories(
        db: Annotated[AsyncSession, Depends(get_db)],
):
    query = select(Category).order_by(Category.name).where(Category.is_active == True)
    categories = await db.scalars(query)
    return categories.all()


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_category(
        session: Annotated[AsyncSession, Depends(get_db)],
        new_category: CreateCategory,
):
    if new_category.parent_id is not None:
        parent = await session.scalar(select(Category).where(Category.id == new_category.parent_id))
        if parent is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Parent category does not exist')

    await session.execute(insert(Category).values(name=new_category.name,
                                       parent_id=new_category.parent_id,
                                       slug=slugify(new_category.name)))
    # category_model = Category(
    #     name=new_category.name,
    #     parent_id=new_category.parent_id,
    #     slug=slugify(new_category.name)
    # )
    # db.add(category_model)

    await session.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }


@router.put('/')
async def update_category(
        session: Annotated[AsyncSession, Depends(get_db)],
        category_slug: str,
        update_category: CreateCategory
):
    query = select(Category).where(Category.slug == category_slug)
    category = await session.scalar(query)
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    await session.execute(update(Category).where(Category.slug == category_slug).values(name=update_category.name,
                                                                                  slug=slugify(update_category.name),
                                                                                  parent_id=category.parent_id,))
    await session.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Category update is successful'
    }

@router.delete('/')
async def delete_category(
        session: Annotated[AsyncSession, Depends(get_db)],
        category_slug: str):
    query = select(Category).where(Category.slug == category_slug, Category.is_active == True)
    category = await session.scalars(query)
    category = category.one_or_none()
    if category:
        category.is_active = False
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Category not found')
    await session.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Category delete is successful'
    }
