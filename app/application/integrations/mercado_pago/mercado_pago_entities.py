from pydantic import BaseModel


class MercadoPagoWebhookPayload(BaseModel):
    id: int
    live_mode: bool
    type: str
    date_created: str
    user_id: int
    api_version: str
    action: str
    data: dict
