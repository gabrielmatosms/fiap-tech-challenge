from abc import ABC
from abc import abstractmethod
from typing import List
from typing import Optional

from app.domain.entities.product import Product
from app.domain.entities.product import ProductCategory
from app.domain.entities.product import ProductDb


class IProductRepository(ABC):
    @abstractmethod
    def add_product(self, product: Product) -> ProductDb:
        pass

    @abstractmethod
    def update_product(self, product_id: int, product: Product) -> Optional[ProductDb]:
        pass

    @abstractmethod
    def delete_product(self, product_id: int) -> bool:
        pass

    @abstractmethod
    def get_products(self, product_ids: Optional[List[int]] = None) -> Optional[ProductDb]:
        pass

    @abstractmethod
    def get_product_by_category(self, category: ProductCategory) -> Optional[ProductDb]:
        pass
