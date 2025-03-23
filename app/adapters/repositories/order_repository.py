import decimal
from typing import List
from typing import Optional

from sqlalchemy import asc
from sqlalchemy import case
from sqlalchemy.orm import Session

from app.adapters.models.order_model import OrderItem
from app.adapters.models.order_model import OrderModel
from app.domain.entities.order import Order
from app.domain.entities.order import OrderDb
from app.domain.entities.order import OrderStatus
from app.domain.entities.payment import PaymentStatus
from app.domain.repositories.order_repository import IOrderRepository


class SQLOrderRepository(IOrderRepository):
    def __init__(self, session: Session):
        self.session = session

    def add_order(self, order: Order, status: OrderStatus, total: str) -> OrderDb:
        try:
            db_order = OrderModel(
                customer_id=order.customer_id,
                status=status.value,
                payment_status=PaymentStatus.PENDING.value,
                total=decimal.Decimal(total),
            )
            self.session.add(db_order)
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise

        try:
            for item in order.items:
                db_item = OrderItem(
                    order_id=db_order.id, product_id=item.product_id, quantity=item.quantity
                )
                self.session.add(db_item)
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise

        self.session.refresh(db_order)
        return OrderDb.from_orm(db_order)

    def cancel_order(self, order_id: int) -> bool:
        order = self.session.query(OrderModel).filter_by(id=order_id).first()
        if not order:
            return False
        order.status = OrderStatus.CANCELED.value
        self.session.commit()
        return True

    def get_order(self, order_id: int) -> Optional[OrderDb]:
        instance = self.session.query(OrderModel).filter_by(id=order_id).first()
        return OrderDb.from_orm(instance) if instance else None

    def get_all_orders(self) -> List[OrderDb]:
        instances = self.session.query(OrderModel).all()
        return [OrderDb.from_orm(instance) for instance in instances]

    def update_order_status(self, order_id: int, status: OrderStatus) -> Optional[OrderDb]:
        order = self.session.query(OrderModel).filter_by(id=order_id).first()
        if not order:
            return None
        order.status = status.value
        self.session.commit()
        self.session.refresh(order)
        return OrderDb.from_orm(order)

    def update_payment_status(
        self, order_id: int, payment_status: PaymentStatus
    ) -> Optional[OrderDb]:
        order = self.session.query(OrderModel).filter_by(id=order_id).first()
        if not order:
            return None
        order.payment_status = payment_status.value
        self.session.commit()
        self.session.refresh(order)
        return OrderDb.from_orm(order)

    def get_filtered_orders(self) -> List[OrderDb]:
        """
        Return orders excluding 'FINALIZED', sorted by:
          1. status priority: READY > PREPARING > RECEIVED
          2. older orders first
        """
        status_priority = case(
            (OrderModel.status == OrderStatus.READY.value, 3),
            (OrderModel.status == OrderStatus.PREPARING.value, 2),
            (OrderModel.status == OrderStatus.RECEIVED.value, 1),
            else_=0,
        )

        query = (
            self.session.query(OrderModel)
            .filter(OrderModel.status != OrderStatus.FINALIZED.value)
            .order_by(status_priority.desc(), asc(OrderModel.created_at))
        )

        instances = query.all()
        return [OrderDb.from_orm(instance) for instance in instances]
