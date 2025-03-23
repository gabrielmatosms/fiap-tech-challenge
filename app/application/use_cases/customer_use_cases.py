from app.adapters.models.session import get_db
from app.adapters.repositories.customer_repository import SQLCustomerRepository
from app.application.exceptions import CpfAlreadyExists
from app.application.exceptions import NotFound
from app.domain.entities.customer import Customer
from app.domain.entities.customer import CustomerDb
from app.domain.repositories.customer_repository import ICustomerRepository


class CustomerUseCases:
    def __init__(self, customer_repository: ICustomerRepository):
        self.customer_repository = customer_repository

    def register_customer(self, customer: Customer) -> CustomerDb:
        existing_customer = self.customer_repository.get_customer_by_cpf(customer.cpf)
        if existing_customer:
            raise CpfAlreadyExists("Customer with this CPF already exists.")
        return self.customer_repository.add_customer(customer)

    def get_customer_by_cpf(self, cpf: str) -> CustomerDb:
        customer = self.customer_repository.get_customer_by_cpf(cpf)
        if not customer:
            raise NotFound("Customer with this CPF not found.")
        return customer

    def get_customer_by_id(self, customer_id: int) -> CustomerDb:
        customer = self.customer_repository.get_customer_by_id(customer_id)
        if not customer:
            raise NotFound("Customer with this ID not found.")
        return customer


def get_customer_use_case() -> CustomerUseCases:
    session = next(get_db())
    repository = SQLCustomerRepository(session=session)
    return CustomerUseCases(repository)
