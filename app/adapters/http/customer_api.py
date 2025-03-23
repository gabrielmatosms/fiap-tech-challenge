from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from starlette import status

from app.application.exceptions import CpfAlreadyExists
from app.application.exceptions import NotFound
from app.application.use_cases.customer_use_cases import CustomerUseCases
from app.application.use_cases.customer_use_cases import get_customer_use_case
from app.domain.entities.customer import Customer
from app.domain.entities.customer import CustomerDb

router = APIRouter()


@router.post("", response_model=CustomerDb)
def register_customer(
    customer: Customer, use_cases: CustomerUseCases = Depends(get_customer_use_case)
):
    try:
        return use_cases.register_customer(customer)
    except CpfAlreadyExists as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("", response_model=CustomerDb)
def get_customer_by_cpf(cpf: str, use_cases: CustomerUseCases = Depends(get_customer_use_case)):
    try:
        return use_cases.get_customer_by_cpf(cpf)
    except NotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
