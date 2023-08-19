from pydantic import BaseModel
from src.domain.aggregates.product.interfaces.product_entity import ProductCategory


class TokenModel(BaseModel):
    access_token: str
    token_type: str


class UpdateProductSchema(BaseModel):
    name: str
    category: ProductCategory
    price: float
    description: str
    uuid: str
