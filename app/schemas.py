from datetime import datetime

from pydantic import BaseModel, Field, EmailStr, field_validator


class CreateProduct(BaseModel):
    '''Модель продукта'''
    name: str = Field(..., min_length=1, max_length=50)
    description: str
    price: int = Field(..., ge=0)
    image_url: str
    stock: int
    category: int
    created_at: datetime = Field(default_factory=datetime.now)

    model_config = {
        "json_schema_extra": {
            "examples":
                [
                    {
                        "name": "Phone",
                        "description": "Simple phone for ringing",
                        "price": "9999",
                        "image_url": "http://some_nice_url.gpg",
                        "stock": "5",
                        "category": "1"
                    }
                ]
        }
    }

class CreateCategory(BaseModel):
    '''Модель категории продукта'''
    name: str
    parent_id: int | None = None

class CreateUser(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    password: str

class CreateReview(BaseModel):
    comment: str
    grade: int
    product_id: int

    @field_validator('grade')
    def validate_grade(cls, v):
        if v < 0 or v > 5:
            raise ValueError('Grade must be between 0 and 5')
        return v
