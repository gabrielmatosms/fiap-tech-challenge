from typing import List
from typing import Optional

from sqlalchemy.orm import Session

from app.adapters.models.product_model import ProductModel
from app.domain.entities.product import Product
from app.domain.entities.product import ProductCategory
from app.domain.entities.product import ProductDb
from app.domain.repositories.product_repository import IProductRepository


class SQLProductRepository(IProductRepository):
    def __init__(self, session: Session):
        self.session = session

    def add_product(self, product: Product) -> ProductDb:
        db_product = ProductModel(**product.model_dump())
        self.session.add(db_product)
        self.session.commit()
        self.session.refresh(db_product)
        return ProductDb.from_orm(db_product)

    def update_product(self, product_id: int, product: Product) -> Optional[ProductDb]:
        db_product = self.session.query(ProductModel).filter_by(id=product_id).first()
        if db_product:
            for attr, value in product.model_dump().items():
                setattr(db_product, attr, value)
            self.session.commit()
            self.session.refresh(db_product)
            return ProductDb.from_orm(db_product)

    def delete_product(self, product_id: int) -> bool:
        db_product = self.session.query(ProductModel).filter_by(id=product_id).first()
        if not db_product:
            return False
        self.session.delete(db_product)
        self.session.commit()
        return True

    def get_products(self, product_ids: Optional[List[int]] = None) -> Optional[ProductDb]:
        query = self.session.query(ProductModel)
        if product_ids:
            query = query.filter(ProductModel.id.in_(product_ids))
        return [ProductDb.from_orm(instance) for instance in query.all()]

    def get_product_by_category(self, category: ProductCategory) -> Optional[ProductDb]:
        instance = self.session.query(ProductModel).filter_by(category=category.value).first()
        return ProductDb.from_orm(instance) if instance else None
