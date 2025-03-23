import decimal
from enum import Enum

from pydantic import BaseModel


class PaymentStatus(str, Enum):
    PENDING = "Pending"
    APPROVED = "Approved"
    DENIED = "Denied"
    REJECTED = "Rejected"
    UNKNOWN = "Unknown"


class QRCodeRequest(BaseModel):
    description: str
    total: decimal.Decimal
    order_id: int
