from app.clients.billing import BillingClient, BillingPaymentResult
from app.clients.kafka import OrderPaymentResultPublisher
from app.modules.models import Order, OrderStatus
from app.modules.repository import OrderRepository
from app.modules.schemas import (
    CreateOrderRequest,
    OrderPaymentResultData,
    OrderPaymentResultEvent,
    OrderPaymentStatus,
    OrderResponse, OrderPaymentResultUpdateDto,
)


class OrderNotFoundError(RuntimeError):
    pass


class OrderService:
    def __init__(
            self,
            repository: OrderRepository,
            billing_client: BillingClient,
            publisher: OrderPaymentResultPublisher,
    ) -> None:
        self.repository = repository
        self.billing_client = billing_client
        self.publisher = publisher

    async def create_order(self, payload: CreateOrderRequest) -> OrderResponse:
        order = await self.repository.create_order(payload.userId, payload.email, payload.price, OrderStatus.PENDING, )
        billing_result = await self.billing_client.withdraw(
            payload.userId,
            payload.price,
        )

        updated_order = await self.repository.update_payment_result(
            OrderPaymentResultUpdateDto(
                id=order.id,
                status=self.get_order_status(billing_result),
                payment_reason=billing_result.reason,
            )
        )

        if updated_order is None:
            raise OrderNotFoundError(f"Order {order.id} not found")

        await self.publisher.publish(self.build_payment_event(updated_order))

        return self.to_order_response(updated_order)

    async def get_order(self, order_id: int) -> OrderResponse:
        order = await self.repository.get_order_by_id(order_id)
        if order is None:
            raise OrderNotFoundError(f"Order {order_id} not found")

        return self.to_order_response(order)

    @staticmethod
    def to_order_response(order: Order) -> OrderResponse:
        return OrderResponse(
            orderId=order.id,
            userId=order.user_id,
            email=order.email,
            price=order.price,
            status=order.status,
            paymentReason=order.payment_reason,
            createdAt=order.created_at,
        )

    @staticmethod
    def build_payment_event(order: Order) -> OrderPaymentResultEvent:
        payment_succeeded = order.status == OrderStatus.PAID
        return OrderPaymentResultEvent(
            subject=f"orders/{order.id}",
            data=OrderPaymentResultData(
                orderId=order.id,
                userId=order.user_id,
                email=order.email,
                price=order.price,
                paymentStatus=(
                    OrderPaymentStatus.SUCCESS
                    if payment_succeeded
                    else OrderPaymentStatus.FAILED
                ),
                message=(
                    "Order paid successfully"
                    if payment_succeeded
                    else "Order payment failed"
                ),
            ),
        )

    @staticmethod
    def get_order_status(billing_result: BillingPaymentResult) -> OrderStatus:
        if billing_result.success:
            return OrderStatus.PAID

        return OrderStatus.PAYMENT_FAILED
