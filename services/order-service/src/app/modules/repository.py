from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.models import Order, OrderStatus
from app.modules.schemas import OrderPaymentResultUpdateDto


class OrderRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_order(
        self,
        user_id: str,
        email: str,
        price,
        status: OrderStatus,
        payment_reason: str | None = None,
    ) -> Order:
        order = Order(
            user_id=user_id,
            email=email,
            price=price,
            status=status,
            payment_reason=payment_reason,
        )
        self.session.add(order)
        await self.session.commit()
        await self.session.refresh(order)
        return order

    async def get_order_by_id(self, order_id: int) -> Order | None:
        result = await self.session.execute(select(Order).where(Order.id == order_id))
        return result.scalar_one_or_none()

    async def update_payment_result(self, dto: OrderPaymentResultUpdateDto) -> Order | None:
        order = await self.get_order_by_id(dto.id)

        if order is None:
            return None

        order.status = dto.status
        order.payment_reason = dto.payment_reason

        await self.session.commit()
        await self.session.refresh(order)
        return order


