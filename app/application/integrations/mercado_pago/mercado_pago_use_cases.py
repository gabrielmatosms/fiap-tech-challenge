import hashlib
import hmac

import requests

from app import config
from app.application.exceptions import QRCodeGenerationError
from app.domain.entities.payment import PaymentStatus
from app.domain.entities.payment import QRCodeRequest


class MercadoPagoUseCases:
    BASE_URL = "https://api.mercadopago.com"
    QR_ENDPOINT = "/instore/orders/qr/seller/collectors"

    def _headers(self):
        return {
            "Authorization": f"Bearer {config.MERCADO_PAGO_ACCESS_TOKEN}",
            "Content-Type": "application/json",
        }

    @staticmethod
    def verify_signature(received_signature: str, request_id: str, data_id: str) -> bool:
        ts_raw, hash_raw = received_signature.split(",")

        ts = ts_raw.split("=")[1]
        hash = hash_raw.split("=")[1]

        manifest = f"id:{data_id};request-id:{request_id};ts:{ts};"  # noqa: E231, E702
        hmac_obj = hmac.new(
            config.MERCADO_PAGO_WEBHOOK_SECRET.encode(),
            msg=manifest.encode(),
            digestmod=hashlib.sha256,
        )

        return hmac_obj.hexdigest() == hash

    def generate_qrcode(self, qr_request: QRCodeRequest) -> str:
        try:
            payload = {
                "title": qr_request.description,
                "external_reference": str(qr_request.order_id),
                "total_amount": float(qr_request.total),
                "description": qr_request.description,
                "cash_out": {
                    "amount": float(qr_request.total),
                },
            }

            url = (
                f"{self.BASE_URL}{self.QR_ENDPOINT}/{config.MERCADO_PAGO_USER_ID}"
                f"/pos/{config.MERCADO_PAGO_POS_ID}/qrs"
            )
            response = requests.post(url, json=payload, headers=self._headers())
            response.raise_for_status()

            return response.json()
        except Exception as e:
            raise QRCodeGenerationError() from e

    def get_payment_status(self, order_id: str) -> PaymentStatus:
        url = f"{self.BASE_URL}/v1/payments/{order_id}"
        response = requests.get(url, headers=self._headers())
        response.raise_for_status()

        try:
            status = response.json()["status"].title()
            return PaymentStatus(status)
        except (KeyError, TypeError):
            return PaymentStatus.UNKNOWN
