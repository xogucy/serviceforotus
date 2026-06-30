from datetime import datetime, timezone
from decimal import Decimal
from enum import StrEnum
from uuid import UUID, uuid4

from pydantic import BaseModel, EmailStr, Field

from app.modules.models import OrderStatus


class CreateOrderRequest(BaseModel):
    userId: str = Field(min_length=1)
    email: EmailStr
    price: Decimal = Field(gt=0)


class OrderResponse(BaseModel):
    orderId: int
    userId: str
    email: EmailStr
    price: Decimal
    status: OrderStatus
    paymentReason: str | None = None
    createdAt: datetime


class OrderPaymentStatus(StrEnum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


class OrderPaymentResultData(BaseModel):
    orderId: int
    userId: str
    email: EmailStr
    price: Decimal
    paymentStatus: OrderPaymentStatus
    message: str


class OrderPaymentResultUpdateDto(BaseModel):
    id: int
    status: OrderStatus
    payment_reason: str | None = None


class OrderPaymentResultEvent(BaseModel):
    specversion: str = "1.0"
    id: UUID = Field(default_factory=uuid4)
    source: str = "/order-service"
    type: str = "ru.otus.orders.payment.result.v1"
    subject: str
    time: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    datacontenttype: str = "application/json"
    data: OrderPaymentResultData
