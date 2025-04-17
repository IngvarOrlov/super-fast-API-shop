from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from slugify import slugify
from app.models import Product, Category
from app.schemas import CreateProduct
from app.backend.db_depends import get_db
from sqlalchemy import select, update, insert, delete
from typing import Annotated
router = APIRouter(prefix='/products', tags=['products'])

@router.get('/')
async def all_products(
        session: AsyncSession = Depends(get_db),
):
    query = select(Product).join(Category).where(
        Product.is_active == True,
        Category.is_active == True,
        Product.stock > 0,
    ).order_by(Product.name)
    products = await session.scalars(query)
    products = products.all()
    if not products:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There are no products")
    return products

@router.post('/')
async def create_product(
        session: Annotated[AsyncSession, Depends(get_db)],
        product: CreateProduct
):
    category = await session.scalar(select(Category).where(Category.id == product.category))
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    slug = slugify(product.name)
    obj_in_db = await session.scalars(select(Product).where(Product.slug == slug))
    obj_in_db = obj_in_db.one_or_none()
    if obj_in_db and obj_in_db.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product already exists")
    elif obj_in_db and obj_in_db.is_active is False:
        query = update(Product).where(Product.slug == slug).values(
            category_id=product.category,
            name=product.name,
            slug=slug,
            description=product.description,
            price=product.price,
            image_url=product.image_url,
            stock=product.stock,
            rating=0.0,
            is_active=True
        )
    else:
        query = insert(Product).values(
        category_id=product.category,
        name=product.name,
        slug=slug,
        description=product.description,
        price=product.price,
        image_url=product.image_url,
        stock=product.stock,
        rating=0.0,
        is_active=True
        )
    await session.execute(query)
    await session.commit()
    return {'status_code': status.HTTP_201_CREATED,
'transaction': 'Successful'}


@router.get('/{category_slug}')
async def product_by_category(
        category_slug: str,
        session: Annotated[AsyncSession, Depends(get_db)],
):
    category = await session.scalar(select(Category).where(Category.slug == category_slug))
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    query = select(Category.id).where(Category.parent_id == category.id)
    categories_corutine = await session.scalars(query)
    categories_ids = [category.id] + categories_corutine.all()
    query = select(Product).where(
        Product.category_id.in_(categories_ids),
                                  Product.is_active == True,
                                  Product.stock > 0
    ).order_by(Product.name)
    products = await session.scalars(query)
    return products.all()

@router.get('/detail/{product_slug}')
async def product_detail(product_slug: str, session: Annotated[AsyncSession, Depends(get_db)]):
    query = select(Product).where(Product.slug == product_slug, Product.is_active == True)
    product = await session.scalar(query)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There is no product found")
    return product


@router.put('/{product_slug}')
async def update_product(product_slug: str, session: Annotated[AsyncSession, Depends(get_db)], product: CreateProduct):
    query = select(Product).where(Product.slug == product_slug, Product.is_active == True)
    old_product = await session.scalar(query)
    if not old_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There is no product found")
    query = update(Product).where(Product.slug == product_slug).values(
        category_id=product.category,
        name=product.name,
        slug=slugify(product.name),
        description=product.description,
        price=product.price,
        image_url=product.image_url,
        stock=product.stock,
        rating=old_product.rating,
        is_active=old_product.is_active

    )
    await session.execute(query)
    await session.commit()

    return {'status_code': status.HTTP_200_OK,
        'transaction': 'Product update is successful'}


@router.delete('/')
async def delete_product(product_id: int, session: Annotated[AsyncSession, Depends(get_db)]):
    query = select(Product).where(Product.id == product_id, Product.is_active == True)
    product = await session.scalar(query)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    query = update(Product).where(Product.id == product_id).values(is_active=False)
    await session.execute(query)
    await session.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'Product delete is successful'}
