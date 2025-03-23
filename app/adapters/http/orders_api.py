from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from starlette import status

from app.application.exceptions import NotFound
from app.application.exceptions import QRCodeGenerationError
from app.application.integrations.mercado_pago.mercado_pago_entities import (
    MercadoPagoWebhookPayload,
)
from app.application.integrations.mercado_pago.mercado_pago_use_cases import MercadoPagoUseCases
from app.application.use_cases.customer_use_cases import CustomerUseCases
from app.application.use_cases.customer_use_cases import get_customer_use_case
from app.application.use_cases.order_use_cases import OrderUseCases
from app.application.use_cases.order_use_cases import get_order_use_case
from app.application.use_cases.product_use_cases import ProductUseCases
from app.application.use_cases.product_use_cases import get_product_use_case
from app.domain.entities.order import Order
from app.domain.entities.order import OrderDb
from app.domain.entities.order import OrderStatus

router = APIRouter()


@router.post("/checkout")
def checkout(
    order: Order,
    use_cases: OrderUseCases = Depends(get_order_use_case),
    mercado_pago_use_cases: MercadoPagoUseCases = Depends(),
    customer_use_cases: CustomerUseCases = Depends(get_customer_use_case),
    product_use_cases: ProductUseCases = Depends(get_product_use_case),
):
    try:
        order, qrcode_link = use_cases.checkout_order(
            order, mercado_pago_use_cases, customer_use_cases, product_use_cases
        )
        return {"order_id": order.id, "qrcode_link": qrcode_link}
    except NotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except QRCodeGenerationError:
        raise HTTPException(status_code=500, detail="Error generating QR code")


@router.get("/{order_id}/payment-status")
def get_payment_status(order_id: int, use_cases: OrderUseCases = Depends(get_order_use_case)):
    status = use_cases.get_payment_status(order_id)
    return {"payment_status": status.value}


@router.post("/payment-webhook")
def payment_webhook(
    request: Request,
    payload: MercadoPagoWebhookPayload,
    order_use_cases: OrderUseCases = Depends(get_order_use_case),
    mercado_pago_use_cases: MercadoPagoUseCases = Depends(),
):
    try:
        order_id = payload.data.get("id")
        x_signature = request.headers.get("x-signature")
        x_request_id = request.headers.get("x-request-id")

        is_valid_signature = mercado_pago_use_cases.verify_signature(
            x_signature, x_request_id, order_id
        )
        if not x_signature or not is_valid_signature:
            raise HTTPException(status_code=400, detail="Invalid or missing signature")

        if payload.get("type") == "payment":
            payment_status = mercado_pago_use_cases.get_payment_status(order_id)
            order_use_cases.update_order_status(order_id, payment_status)

        return {}
    except Exception:
        raise HTTPException(status_code=500, detail="Error processing webhook")


@router.get("/get-filtered-orders", response_model=List[OrderDb])
def get_custom_order_list(use_cases: OrderUseCases = Depends(get_order_use_case)):
    return use_cases.get_filtered_orders()


@router.put("/{order_id}/status", response_model=OrderDb)
def update_order_status(
    order_id: int, new_status: OrderStatus, use_cases: OrderUseCases = Depends(get_order_use_case)
):
    updated_order = use_cases.update_order_status(order_id, new_status)
    if not updated_order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return updated_order


@router.get("/{order_id}", response_model=OrderDb)
def get_order(order_id: int, use_cases: OrderUseCases = Depends(get_order_use_case)):
    order = use_cases.get_order(order_id)
    if order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order


@router.get("", response_model=List[OrderDb])
def get_all_orders(use_cases: OrderUseCases = Depends(get_order_use_case)):
    return use_cases.get_all_orders()
