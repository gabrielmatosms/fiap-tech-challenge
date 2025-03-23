from abc import ABC
from abc import abstractmethod
from typing import Optional

from app.domain.entities.customer import Customer
from app.domain.entities.customer import CustomerDb


class ICustomerRepository(ABC):
    @abstractmethod
    def add_customer(self, customer: Customer) -> CustomerDb:
        pass

    @abstractmethod
    def get_customer_by_cpf(self, cpf: str) -> Optional[CustomerDb]:
        pass

    @abstractmethod
    def get_customer_by_id(self, customer_id: int) -> Optional[CustomerDb]:
        pass
