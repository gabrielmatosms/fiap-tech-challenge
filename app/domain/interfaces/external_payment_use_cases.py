from abc import ABC
from abc import abstractmethod

from app.domain.entities.payment import PaymentStatus
from app.domain.entities.payment import QRCodeRequest


class IExternalPaymentUseCase(ABC):
    @abstractmethod
    def generate_qrcode(self, qr_request: QRCodeRequest) -> str:
        pass

    @abstractmethod
    def get_payment_status(self, payload: dict) -> PaymentStatus:
        pass
