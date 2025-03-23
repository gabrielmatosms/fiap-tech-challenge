from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from starlette import status

from app.application.use_cases.product_use_cases import ProductUseCases
from app.application.use_cases.product_use_cases import get_product_use_case
from app.domain.entities.product import Product
from app.domain.entities.product import ProductCategory
from app.domain.entities.product import ProductDb

router = APIRouter()


@router.post("", response_model=ProductDb)
def add_product(product: Product, use_cases: ProductUseCases = Depends(get_product_use_case)):
    return use_cases.add_product(product)


@router.put("/{product_id}", response_model=ProductDb)
def update_product(
    product_id: int, product: Product, use_cases: ProductUseCases = Depends(get_product_use_case)
):
    updated_product = use_cases.update_product(product_id, product)
    if updated_product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return updated_product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, use_cases: ProductUseCases = Depends(get_product_use_case)):
    success = use_cases.delete_product(product_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return {}


@router.get("", response_model=List[ProductDb])
def get_all_products(use_cases: ProductUseCases = Depends(get_product_use_case)):
    return use_cases.get_products()


@router.get("/{category}", response_model=ProductDb)
def get_product_by_category(
    category: ProductCategory, use_cases: ProductUseCases = Depends(get_product_use_case)
):
    product = use_cases.get_product_by_category(category)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product
