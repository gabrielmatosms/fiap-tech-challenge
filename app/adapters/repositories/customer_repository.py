from typing import Optional

from sqlalchemy.orm import Session

from app.adapters.models.customer_model import CustomerModel
from app.domain.entities.customer import Customer
from app.domain.entities.customer import CustomerDb
from app.domain.repositories.customer_repository import ICustomerRepository


class SQLCustomerRepository(ICustomerRepository):
    def __init__(self, session: Session):
        self.session = session

    def add_customer(self, customer: Customer) -> CustomerDb:
        instance = CustomerModel(**customer.model_dump())
        self.session.add(instance)
        self.session.commit()
        self.session.refresh(instance)
        return CustomerDb.from_orm(instance)

    def get_customer_by_cpf(self, cpf: str) -> Optional[CustomerDb]:
        instance = self.session.query(CustomerModel).filter_by(cpf=cpf).first()
        return CustomerDb.from_orm(instance) if instance else None

    def get_customer_by_id(self, customer_id: int) -> Optional[CustomerDb]:
        instance = self.session.query(CustomerModel).filter_by(id=customer_id).first()
        return CustomerDb.from_orm(instance) if instance else None
