from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.clients.billing import BillingClient
from app.clients.kafka import OrderPaymentResultPublisher
from app.core.config import get_settings
from app.db.session import get_session
from app.modules.repository import OrderRepository
from app.modules.service import OrderService


def get_order_service(
    session: AsyncSession = Depends(get_session),
) -> OrderService:
    settings = get_settings()
    repository = OrderRepository(session)
    billing_client = BillingClient(settings.billing_service_url)
    publisher = OrderPaymentResultPublisher(
        bootstrap_servers=settings.kafka_bootstrap_servers,
        topic=settings.order_payment_result_topic,
    )
    return OrderService(repository, billing_client, publisher)
