from typing import List
from typing import Optional

from app.adapters.models.session import get_db
from app.adapters.repositories.product_repository import SQLProductRepository
from app.domain.entities.product import Product
from app.domain.entities.product import ProductCategory
from app.domain.entities.product import ProductDb
from app.domain.repositories.product_repository import IProductRepository


class ProductUseCases:
    def __init__(self, product_repository: IProductRepository):
        self.product_repository = product_repository

    def add_product(self, product: Product) -> ProductDb:
        return self.product_repository.add_product(product)

    def update_product(self, product_id: int, product: Product) -> Optional[ProductDb]:
        return self.product_repository.update_product(product_id, product)

    def delete_product(self, product_id: int) -> bool:
        return self.product_repository.delete_product(product_id)

    def get_products(self, product_ids: Optional[List[int]] = None) -> List[ProductDb]:
        return self.product_repository.get_products(product_ids)

    def get_product_by_category(self, category: ProductCategory) -> Optional[ProductDb]:
        return self.product_repository.get_product_by_category(category)


def get_product_use_case() -> ProductUseCases:
    session = next(get_db())
    repository = SQLProductRepository(session=session)
    return ProductUseCases(repository)
